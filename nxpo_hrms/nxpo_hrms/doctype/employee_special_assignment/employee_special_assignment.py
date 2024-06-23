# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today
from dateutil.relativedelta import relativedelta


class EmployeeSpecialAssignment(Document):
	
	def validate(self):
		self.validate_date()
		self.update_business_unit_data()
		self.update_duration()
		self.update_active()
	
	def on_update(self):
		self.reload()

	def validate_date(self):
		""" Ensure that to_date is greater than from_date """
		if self.to_date and self.from_date > self.to_date:
			frappe.throw(_("From Date must be before To Date"))

	def update_duration(self):
		if not self:
			return
		duration = None
		if self.to_date and self.from_date and self.to_date:
			diff = relativedelta(getdate(self.to_date), getdate(self.from_date))
			duration = "{0} Years {1} Months {2} Days".format(
				diff.years, diff.months, diff.days
			)
		self.duration = duration
	
	def update_active(self):
		to_date = self.to_date if self.to_date else today()
		if getdate(today()) >= getdate(self.from_date) and getdate(today()) <= getdate(to_date):
			self.active = 1
		else:
			self.active = 0
		
	def	update_business_unit_data(self):
		subdepartment = None
		department = None
		directorate = None
		if self.business_unit:
			type = frappe.db.get_value("Department", self.business_unit, "custom_type")
			if type == "แผนกงาน":
				subdepartment = self.business_unit
				department = frappe.db.get_value("Department", subdepartment, "parent_department")
				directorate = frappe.db.get_value("Department", department, "parent_department")
			if type == "ฝ่ายงาน":
				department = self.business_unit
				directorate = frappe.db.get_value("Department", department, "parent_department")
			if type == "กลุ่มงาน":
				directorate = self.business_unit
		self.subdepartment = subdepartment,
		self.department = department
		self.directorate = directorate


def job_update_active():
	names = frappe.db.get_all(
		"Employee Special Assignment",
		pluck="name"
	)
	for name in names:
		doc = frappe.get_doc("Employee Special Assignment", name)
		doc.update_active()
		doc.save()
		frappe.db.commit()
