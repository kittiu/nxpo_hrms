# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import json
import frappe
from frappe import _

class BankPaymentExport(Document):

    def on_submit(self):
        if not self.bank_sal_slip:
            frappe.throw(_("Submission Error: No salary slips found in the bank payment export."))

    @frappe.whitelist()
    def fill_sal_slip(self):
        filters = frappe._dict(
            posting_date=self.posting_date,
            nob=self.type,
        )
        sal_slip = get_sal_slip(filters)
        self.set("bank_sal_slip", [])
        if not sal_slip:
            error_msg = _("No Salary Slip From This Posting Date")
            frappe.throw(error_msg, title=_("No Salary Slip found"))
        self.set("bank_sal_slip", sal_slip)


def get_sal_slip(filters):
    data = []
    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""
            select
                ss.name as salary_slip,
                ss.employee as employee
            from `tabSalary Slip` ss
            where ss.docstatus = 1
            {('AND ' + conditions) if conditions else ''}
        """,
        filters,
        as_dict=True,
    )
    data = query_data

    return data

def get_conditions(filters):
    conditions = []
    if filters.get("nob") == 'Normal':
        conditions.append("ss.posting_date = %(posting_date)s")

    if filters.get("nob") == 'Bonus':
        conditions.append("ss.custom_date_for_split_tax_component = %(posting_date)s")


    # Combine conditions into a single string
    return " AND ".join(conditions)