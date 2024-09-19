# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
import datetime

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
    date_diff,
    flt,
    getdate,
    today
)
from datetime import timedelta

from frappe.desk.form.assign_to import add as add_assignment
from collections import Counter
from hrms.hr.doctype.leave_application.leave_application import get_holidays



class OffsiteWorkRequest(Document):

    def validate(self):

        holiday_list = frappe.db.get_value('Company', self.company, 'default_holiday_list')
        # 1. Check negative days
        for plan in self.plan_dates:
            # plan.days = (getdate(plan.to_date) - getdate(plan.from_date)).days + 1
            plan.days = self.get_number_of_leave_days_for_owr(plan.from_date, plan.to_date, self.employee, holiday_list)
            if plan.days <= 0:
                frappe.throw(_("To Date before From Date is not allowed!"))
        # Total days
        self.total_days = sum([x.days for x in self.plan_dates])
        
        dates = []
        # 2. Check overlaps dates
        for plan in self.plan_dates:
            dates += [
                getdate(plan.from_date) + timedelta(days=x)
                for x in range((getdate(plan.to_date) - getdate(plan.from_date)).days + 1)
            ]
        overlap_dates = self.get_date_overlap_remove_holiday(holiday_list, dates)
        unique_days = len(list(set(overlap_dates)))
        if unique_days != self.total_days:
            frappe.throw(_("Please make sure that all selected dates are not overlapping"))
        
        # 3. Validate no more than OWR policy
        self.validate_owr_policy(overlap_dates)

        # 4. Validate half day date
        for plan in self.plan_dates:
            if plan.half_day:
                if not getdate(plan.from_date) <= getdate(plan.half_day_date) <= getdate(plan.to_date):
                    frappe.throw(_("Half day date should be in between from date and to date"))
            else:
                plan.half_day_date = None
        
        # 5. For backdate request, no future date allowed.
        if self.type == "Backdate Request":
            if any([
                getdate(plan.from_date) > getdate(today())
                or getdate(plan.to_date) > getdate(today())
                for plan in self.plan_dates
            ]):
                frappe.throw(_("Backdate request should not have future date"))

    def on_submit(self):
        # Validate
        for plan in self.plan_dates:
            doc = frappe.new_doc("Attendance Request")
            doc.employee = self.employee
            doc.from_date = plan.from_date
            doc.to_date = plan.to_date
            doc.validate_request_overlap()
        # Set Pending
        self.db_set("status", "Pending")

    def on_cancel(self):
        self.db_set("status", "Cancelled")

    def validate_owr_policy(self, dates):
        owr_days_per_week = frappe.get_cached_value("Company", self.company, "custom_owr_days_per_week")
        # Get weeks from Offsite Work Request
        week_list = list(map(lambda d: d.isocalendar()[1], dates))
        # Get weeks from existing OWR attendance
        Attendance = frappe.qb.DocType("Attendance")
        owr_dates = (
            frappe.qb.from_(Attendance)
            .select(Attendance.attendance_date)
            .where(
                (Attendance.employee == self.employee)
                & (Attendance.docstatus < 2)
                & (Attendance.status == "Work From Home")
            )
        ).run()
        owr_dates = [d[0] for d in owr_dates]
        week_list += list(map(lambda d: d.isocalendar()[1], owr_dates))
        week_exceed = [str(k) for (k, v) in Counter(week_list).items() if v > owr_days_per_week]
        if week_exceed and self.type == "Work From Anywhere":
            frappe.throw(
                _("Your Offsite Work Request is exceeding {} days on the week {}").format(
                    owr_days_per_week,
                    ", ".join(week_exceed)
                )
            )

    @frappe.whitelist()
    def create_attendance_requests(self):
        try:
            reason = "Work From Home"
            if self.type == "Backdate Request":
                reason = "On Duty"
            for plan in self.plan_dates:
                attend = frappe.new_doc("Attendance Request")
                attend.update({
                    "employee": self.employee,
                    "company": self.company,
                    "from_date": plan.from_date,
                    "to_date": plan.to_date,
                    "reason": reason,
                    "explanation": self.note,
                    "half_day": plan.half_day,
                    "half_day_date": plan.half_day_date,
                    "custom_offsite_work_request": self.name,
                })
                attend.submit()
            self.db_set("status", "Completed")
            self.add_comment("Label", _("Created Offsite Work Request as attendances"))
        except Exception as e:
            frappe.db.rollback()
            self.db_set("status", "Pending")
            self.add_comment("Label", _("Failed create Offsite Work Request as attendances: {}").format(str(e)))

    @frappe.whitelist()
    def get_number_of_leave_days_for_owr(
        self,
        from_date: datetime.date,
        to_date: datetime.date,
        employee: str| None = None,
        holiday_list: str | None = None,
    ) -> float:
        number_of_days = 0
        number_of_days = date_diff(to_date, from_date) + 1
        number_of_days = flt(number_of_days) - flt(
                get_holidays(employee, from_date, to_date, holiday_list=holiday_list)
            )
        return number_of_days
    
    @frappe.whitelist()
    def get_date_overlap_remove_holiday(self, holiday_list, dates):
        holiday_all = frappe.db.get_all(
            "Holiday",
            filters={
                "parent": holiday_list,
            },
            pluck="holiday_date"
        )

        holiday_set = set(holiday_all)
        dates_set = set(dates)

        # Find matching dates (overlaps)
        overlapping_dates = dates_set & holiday_set
        # Remove overlapping dates from the original list
        updated_dates_set = dates_set - overlapping_dates
        # Convert the updated set back to a list if needed
        updated_dates = list(updated_dates_set)

        return updated_dates

    @frappe.whitelist()
    def get_sum_total_days(self, holiday_list):
        for plan in self.plan_dates:
            plan.days = self.get_number_of_leave_days_for_owr(plan.from_date, plan.to_date, self.employee, holiday_list)
            if plan.days <= 0:
                frappe.throw(_("To Date before From Date is not allowed!"))
        self.total_days = sum([x.days for x in self.plan_dates])
        return self.total_days


def auto_create_attendance_requests():
    # Find all Offsite Work Requested submitted but not completed
    docs = frappe.db.get_all(
        "Offsite Work Request",
        filters={
            "docstatus": 1,
            "status": "Pending",
        },
        pluck="name"
    )
    for doc_name in docs:
        doc = frappe.get_doc("Offsite Work Request", doc_name)
        doc.create_attendance_requests()
        frappe.db.commit()
