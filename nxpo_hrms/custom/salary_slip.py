# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _


def validate_no_salary(doc, method=None):
    employment_type = frappe.db.get_value("Employee", doc.employee, "employment_type")
    if frappe.db.get_value("Employment Type", employment_type, "custom_no_salary"):
        frappe.throw(_("Cannot create Salary Slip for Employee with Employee Type - No Salary"))
