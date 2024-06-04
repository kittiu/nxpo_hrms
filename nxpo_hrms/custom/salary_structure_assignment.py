# License: GNU General Public License v3. See license.txt
import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment


class SalaryStructureAssignmentNXPO(SalaryStructureAssignment):

    def validate(self):
        allow = self.custom_allow_salary_assignment
        temp_date = None
        if allow:
            temp_date = frappe.db.get_value("Employee", self.employee, "relieving_date")
            frappe.db.set_value("Employee", self.employee, "relieving_date", None)
        super().validate()
        if allow:
            frappe.db.set_value("Employee", self.employee, "relieving_date", temp_date)
