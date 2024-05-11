# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import timedelta


class WFHRequest(Document):

	def validate(self):
		# Check negative days
		for plan in self.plan_dates:
			plan.days = (getdate(plan.to_date) - getdate(plan.from_date)).days + 1
			if plan.days <= 0:
				frappe.throw(_("To Date before From Date is not allowed!"))
		# Total days
		self.total_days = sum([x.days for x in self.plan_dates])
		# Check overlaps dates
		dates = []
		for plan in self.plan_dates:
			dates += [
				getdate(plan.from_date) + timedelta(days=x)
				for x in range((getdate(plan.to_date) - getdate(plan.from_date)).days + 1)
			]
		unique_days = len(list(set(dates)))
		if unique_days != self.total_days:
			frappe.throw(_("Please make sure that all selected dates are not overlapping"))

	def on_submit(self):
		for plan in self.plan_dates:
			doc = frappe.new_doc("Attendance Request")
			doc.employee = self.employee
			doc.from_date = plan.from_date
			doc.to_date = plan.to_date
			doc.validate_request_overlap()
		self.db_set("status", "Pending")
	
	def on_cancel(self):
		self.db_set("status", "Cancelled")
	
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
