# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.utils import date_diff


def validate_no_salary(doc, method=None):
    no_salary = frappe.db.get_value("Employee", doc.employee, "custom_no_salary")
    if no_salary:
        frappe.throw(_("Cannot create Salary Slip for Employee with Employee Type - No Salary"))
