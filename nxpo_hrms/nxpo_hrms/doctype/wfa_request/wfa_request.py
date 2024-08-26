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
)
from datetime import timedelta

from frappe.desk.form.assign_to import add as add_assignment
from collections import Counter
from hrms.hr.doctype.leave_application.leave_application import get_holidays



class WFARequest(Document):

	def validate(self):
		# 1. Check negative days
		for plan in self.plan_dates:
			plan.days = (getdate(plan.to_date) - getdate(plan.from_date)).days + 1
			if plan.days <= 0:
				frappe.throw(_("To Date before From Date is not allowed!"))
		# Total days
		self.total_days = sum([x.days for x in self.plan_dates])

		# 2. Check overlaps dates
		dates = []
		for plan in self.plan_dates:
			dates += [
				getdate(plan.from_date) + timedelta(days=x)
				for x in range((getdate(plan.to_date) - getdate(plan.from_date)).days + 1)
			]
		unique_days = len(list(set(dates)))
		if unique_days != self.total_days:
			frappe.throw(_("Please make sure that all selected dates are not overlapping"))
		
		# 3. Validate no more than WFA policy
		self.validate_wfa_policy(dates)

		# 4. Validate half day date
		for plan in self.plan_dates:
			if plan.half_day:
				if not getdate(plan.from_date) <= getdate(plan.half_day_date) <= getdate(plan.to_date):
					frappe.throw(_("Half day date should be in between from date and to date"))
			else:
				plan.half_day_date = None

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
		# Assign Approver to get notified
		add_assignment({
			"assign_to": [self.approver],
			"doctype": self.doctype,
			"name": self.name,
			"description": self.note,
		})

	def on_cancel(self):
		self.db_set("status", "Cancelled")

	def validate_wfa_policy(self, dates):
		wfa_days_per_week = frappe.get_cached_value("Company", self.company, "custom_wfa_days_per_week")
		# Get weeks from WFA request
		week_list = list(map(lambda d: d.isocalendar()[1], dates))
		# Get weeks from existing WFA attendance
		Attendance = frappe.qb.DocType("Attendance")
		wfa_dates = (
			frappe.qb.from_(Attendance)
			.select(Attendance.attendance_date)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.status == "Work From Home")
			)
		).run()
		wfa_dates = [d[0] for d in wfa_dates]
		week_list += list(map(lambda d: d.isocalendar()[1], wfa_dates))
		week_exceed = [str(k) for (k, v) in Counter(week_list).items() if v > wfa_days_per_week]
		if week_exceed:
			frappe.throw(
				_("Your WFA request is exceeding {} days on the week {}").format(
					wfa_days_per_week,
					", ".join(week_exceed)
				)
			)

	@frappe.whitelist()
	def create_attendance_requests(self):
		try:
			for plan in self.plan_dates:
				attend = frappe.new_doc("Attendance Request")
				attend.update({
					"employee": self.employee,
					"company": self.company,
					"from_date": plan.from_date,
					"to_date": plan.to_date,
					"reason": "Work From Home",
					"explanation": self.note,
					"half_day": plan.half_day,
					"half_day_date": plan.half_day_date,
					"custom_wfa_request": self.name,
				})
				attend.submit()
			self.db_set("status", "Completed")
			self.add_comment("Label", _("Created WFA Request as attendances"))
		except Exception as e:
			frappe.db.rollback()
			self.db_set("status", "Pending")
			self.add_comment("Label", _("Failed create WFA Request as attendances: {}").format(str(e)))

	@frappe.whitelist()
	def get_number_of_leave_days_for_wfa(
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

def auto_create_attendance_requests():
	# Find all WFA requested submitted but not completed
	docs = frappe.db.get_all(
		"WFA Request",
		filters={
			"docstatus": 1,
			"status": "Pending",
		},
		pluck="name"
	)
	for doc_name in docs:
		doc = frappe.get_doc("WFA Request", doc_name)
		doc.create_attendance_requests()
		frappe.db.commit()
