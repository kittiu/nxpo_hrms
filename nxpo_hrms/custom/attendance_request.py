# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe

def validate_status_wfh(doc, method):
	# If reason is Work From Home, pass this flag to Attendance
	if doc.reason == "Work From Home":
		frappe.flags.is_work_from_anywhere = True
