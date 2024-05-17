# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import timedelta
from frappe.desk.form.assign_to import add as add_assignment
from collections import Counter


class WFHRequest(Document):

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
		
		# 3. Validate no more than WFH policy
		self.validate_wfh_policy(dates)

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

	def validate_wfh_policy(self, dates):
		wfh_days_per_week = frappe.get_cached_value("Company", self.company, "custom_wfh_days_per_week")
		# Get weeks from WFH request
		week_list = list(map(lambda d: d.isocalendar()[1], dates))
		# Get weeks from existing WFH attendance
		Attendance = frappe.qb.DocType("Attendance")
		wfh_dates = (
			frappe.qb.from_(Attendance)
			.select(Attendance.attendance_date)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.status == "Work From Home")
			)
		).run()
		wfh_dates = [d[0] for d in wfh_dates]
		week_list += list(map(lambda d: d.isocalendar()[1], wfh_dates))
		week_exceed = [str(k) for (k, v) in Counter(week_list).items() if v > wfh_days_per_week]
		if week_exceed:
			frappe.throw(
				_("Your WFH request is exceeding {} days on the week {}").format(
					wfh_days_per_week,
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
					"custom_wfh_request": self.name,
				})
				attend.submit()
			self.db_set("status", "Completed")
			self.add_comment("Label", _("Created WFH Request as attendances"))
		except Exception as e:
			frappe.db.rollback()
			self.db_set("status", "Pending")
			self.add_comment("Label", _("Failed create WFH Request as attendances: {}").format(str(e)))

def auto_create_attendance_requests():
	# Find all WFH requested submitted but not completed
	docs = frappe.db.get_all(
		"WFH Request",
		filters={
			"docstatus": 1,
			"status": "Pending",
		},
		pluck="name"
	)
	for doc_name in docs:
		doc = frappe.get_doc("WFH Request", doc_name)
		doc.create_attendance_requests()
		frappe.db.commit()
