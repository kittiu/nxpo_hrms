# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe

def validate_status_wfh(doc, method):
	if doc.status == "Work From Home":
		doc.status = "Present"
		doc.custom_work_from_anywhere = 1
	elif doc.status in ("Absent", "On Leave"):
		doc.custom_work_from_anywhere = 0
	elif frappe.flags.is_work_from_anywhere:
		doc.custom_work_from_anywhere = 1



