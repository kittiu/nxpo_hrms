# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from thai_payroll.custom.salary_slip import SalarySlipThaiPayroll
from hrms.payroll.doctype.salary_slip.salary_slip import calculate_tax_by_tax_slab


class SalarySlipNXPO(SalarySlipThaiPayroll):

    def autoname(self):
        # Do not set name for Salary Slip, use custom field naming_series instead
        pass

    def calculate_variable_based_on_taxable_salary(self, tax_component):
        tax_amount = super().calculate_variable_based_on_taxable_salary(tax_component)
        split_amount = self.calculate_split_tax(tax_component, self.total_structured_tax_amount)
        self.custom_split_tax_deduct_amount = split_amount
        self.custom_main_tax_deduct_amount = tax_amount - split_amount
        return tax_amount


    def calculate_split_tax(self, tax_component, total_structured_tax_amount):
        eval_locals, default_data = self.get_data_for_eval()
        # Total taxable earnings with spliting addl earning with full tax
        if not self.custom_split_tax_deduction_on:
            return 0.0
        split_tax_addl_earning = 0.0
        for e in self.earnings:
            # Only addional earning with full tax is eligible
            if not (
                e.is_tax_applicable and
                e.additional_salary and
                e.deduct_full_tax_on_selected_payroll_date
            ):
                continue
            # Match with Split Tax Deduction On
            if e.salary_component == self.custom_split_tax_deduction_on:
                split_tax_addl_earning += e.amount
        if split_tax_addl_earning:
            earnings = (
                self.total_taxable_earnings_without_full_tax_addl_components +
                split_tax_addl_earning
            )
            split_addl_earning_tax = calculate_tax_by_tax_slab(
                earnings, self.tax_slab, self.whitelisted_globals, eval_locals
            )
            # Return only tax amount on split tax earning component
            return split_addl_earning_tax - total_structured_tax_amount
        return 0.0


def validate_no_salary(doc, method=None):
    no_salary = frappe.db.get_value("Employee", doc.employee, "custom_no_salary")
    if no_salary:
        frappe.throw(_("Cannot create Salary Slip for Employee with Employee Type - No Salary"))


def get_permission_query_conditions(user):
    # This script ensure that only user with rol Payroll User can access all Salary Slips
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name", cache=True)
    restrict = "employee = %s" % frappe.db.escape(employee)
    roles = frappe.db.get_all("Has Role", filters=dict(parent=user), pluck="role")
    if "Payroll User" in roles:
        restrict = ""
    return restrict

def set_print_format_as_custom():
    # Set as custom, so user can disable it in production
    print_formats = [
        "Salary Slip Excluded Bonus EN",
        "Salary Slip Excluded Bonus TH",
        "Salary Slip Bonus Paid EN",
        "Additional Salary Period Slip EN",
        "Salary Slip Bonus Paid TH",
        "Additional Salary Period Slip TH",
        "Tax Computation Report",
        "Salary Slip with Year to Date",
        "Salary Slip based on Timesheet",
        "Salary Slip Standard",
    ]
    for print_format in print_formats:
        frappe.db.set_value("Print Format", print_format, "standard", "No")
