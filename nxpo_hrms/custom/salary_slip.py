# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.utils import date_diff
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_slip.salary_slip import calculate_tax_by_tax_slab


class SalarySlipNXPO(SalarySlip):

    def calculate_variable_based_on_taxable_salary(self, tax_component):
        tax_amount = super().calculate_variable_based_on_taxable_salary(tax_component)
        split_tax_amount = self.calculate_split_tax(tax_component, self.total_structured_tax_amount)
        for d in self.deductions:
            if d.custom_split_tax_deduction_for:
                self.remove(d)
        # Passing values to add_tax_components()
        frappe.flags.split_tax_amount = split_tax_amount
        frappe.flags.split_tax_component = tax_component
        # --
        return tax_amount - split_tax_amount
    
    def add_tax_components(self):
        super().add_tax_components()
        if frappe.flags.split_tax_amount:
            self.append("deductions",
                {
                    "salary_component": frappe.flags.split_tax_component,
                    "amount": frappe.flags.split_tax_amount,
                    "custom_split_tax_deduction_for": self.custom_split_tax_deduction_on,
                }
            )

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
