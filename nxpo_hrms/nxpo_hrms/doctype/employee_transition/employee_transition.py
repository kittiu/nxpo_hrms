# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta


class EmployeeTransition(Document):
	
	def validate(self):
		# Validate for future date only
		self.validate_transition_date()
		# Get valid previous transition data
		prev = self.get_previous_transition_data()
		self.update(prev)
		bu = self.get_business_unit_data(prev.previous_business_unit)
		self.previous_subdepartment = bu.subdepartment
		self.previous_department = bu.department
		self.previous_directorate = bu.directorate
		# Validate business unit
		bu = self.get_business_unit_data(self.business_unit)
		self.update(bu)
	
	def on_submit(self):
		# Update end date on previous transaction
		if self.previous_transition:
			prev = frappe.get_doc("Employee Transition", self.previous_transition)
			prev.update_end_date()
			prev.update_duration()
		# Update current designation and department
		self.update_employee_position()

	def on_update_after_submit(self):
		self.update_end_date()
		self.update_duration()
	
	def on_cancel(self):
		if self.previous_transition:
			# Remove end date on previous transaction
			prev = frappe.get_doc("Employee Transition", self.previous_transition)
			prev.update_end_date()
			prev.update_duration()
		# Revert current designation and department
		self.revert_employee_position()

	def validate_transition_date(self):
		"""
		For the same employee,
		- Transition Date must not duplicated
		- Transition Date should be latest
		"""
		# Check Transition Date
		transition_date = frappe.db.get_value(
			"Employee Transition",
			{
				"employee": self.employee,
				"docstatus": 1,
				"transition_date": self.transition_date,
				"name": ("!=", self.name),
			},
			"transition_date",
		)
		if transition_date:
			frappe.throw(
				_("Transition Date must not be duplicated for the same Employee"),
				title="Duplicate Transition Date",
			)
		# Check Transition Date is the latest
		previous_transition_date = frappe.db.get_value(
			"Employee Transition",
			{
				"employee": self.employee,
				"docstatus": 1,
				"transition_date": (">", self.transition_date),
			},
			"transition_date",
			order_by="transition_date",
		)
		if previous_transition_date:
			frappe.throw(
				_("Transition Date should be greater than previous Transition Date"),
				title=_("Invalid Transition Date"),
			)

	def get_previous_transition_data(self):
		"""
		Find the previous latest Employee Transition baed on Transition Date,
		if found, set it as Previous Transition
		"""
		ts = frappe.db.get_value(
			"Employee Transition",
			{
				"employee": self.employee,
				"transition_date": ("<", self.transition_date),
				"docstatus": 1,
			},
			["name", "designation", "business_unit"],
			order_by="transition_date desc",
		)
		return frappe._dict({
			"previous_transition": ts and ts[0] or None,
			"previous_designation": ts and ts[1] or None,
			"previous_business_unit": ts and ts[2] or None,
		})
		
	def update_end_date(self):
		"""
		If field set_end_date_manually is not set, set end_date to next Employee Transition,
		If set_end_date_manually is set, do nothing as user will set it manually
		"""
		if not self:
			return
		if not self.set_end_date_manually:
			transition_date = frappe.db.get_value(
				"Employee Transition",
				{
					"employee": self.employee,
					"previous_transition": self.name,
					"docstatus": 1,
				},
				"transition_date",
				order_by="transition_date",
			)
			end_date = getdate(transition_date) if transition_date else None
			frappe.db.set_value("Employee Transition", self.name, "end_date", end_date)
		self.reload()

	def update_duration(self):
		"""
		Get duration between End Date and Transition Date
		"""
		if not self:
			return
		duration = None
		if self.end_date and self.transition_date:
			diff = relativedelta(getdate(self.end_date), getdate(self.transition_date))
			duration = "{0} Years {1} Months {2} Days".format(
				diff.years, diff.months, diff.days
			)
		frappe.db.set_value("Employee Transition", self.name, "duration", duration)
		self.reload()
	
	def update_employee_position(self):
		emp = frappe.get_doc("Employee", self.employee)
		emp.designation = self.designation
		des = frappe.get_doc("Designation", emp.designation)
		emp.custom_job_family = des.custom_job_family
		emp.grade = des.custom_personal_grade
		emp.custom_job_family = des.custom_job_family
		emp.grade = des.custom_personal_grade
		emp.custom_subdepartment = self.subdepartment
		emp.department = self.department
		emp.custom_directorate = self.directorate
		emp.save()

	def revert_employee_position(self):
		emp = frappe.get_doc("Employee", self.employee)
		emp.designation = self.previous_designation
		if emp.designation:
			des = frappe.get_doc("Designation", emp.designation)
			emp.custom_job_family = des.custom_job_family
			emp.grade = des.custom_personal_grade
		else:
			emp.custom_job_family = None
			emp.grade = None
		emp.custom_subdepartment = self.previous_subdepartment
		emp.department = self.previous_department
		emp.custom_directorate = self.previous_directorate
		emp.save()
	
	def	get_business_unit_data(self, business_unit):
		subdepartment = None
		department = None
		directorate = None
		if business_unit:
			type = frappe.db.get_value("Department", business_unit, "custom_type")
			if type == "แผนกงาน":
				subdepartment = business_unit
				department = frappe.db.get_value("Department", subdepartment, "parent_department")
				directorate = frappe.db.get_value("Department", department, "parent_department")
			if type == "ฝ่ายงาน":
				department = business_unit
				directorate = frappe.db.get_value("Department", department, "parent_department")
			if type == "กลุ่มงาน":
				directorate = business_unit
		return frappe._dict({
			"subdepartment": subdepartment,
			"department": department,
			"directorate": directorate
		})

