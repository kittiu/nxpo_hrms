# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.utils.nestedset import get_root_of


def validate_department(doc, method):
	"""
	If custom_type = "แผนกงาน" then custom_chief and custom_assistant are not allowed
	If custom_type = "ฝ่ายงาน" then custom_chief is required but custom_assistant is not allowed
	If custom_type = "กลุ่มงาน" then custom_chief and custom_assistant are required
	"""
	if doc.custom_type == "แผนกงาน":
		if doc.custom_chief or doc.custom_assistant:
			frappe.throw(_("Chief and Assistant are not allowed for {0}").format("แผนกงาน"))
	if doc.custom_type == "ฝ่ายงาน":
		if not doc.custom_chief:
			frappe.throw(_("Chief is required for {0}").format("ฝ่ายงาน"))
		if doc.custom_assistant:
			frappe.throw(_("Assistant is not allowed for {0}").format("ฝ่ายงาน"))
	if doc.custom_type == "กลุ่มงาน":
		if not doc.custom_chief or not doc.custom_assistant:
			frappe.throw(_("Chief and Assistant are required for {0}").format("กลุ่มงาน"))


@frappe.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	fields = ["name as value", "is_group as expandable"]
	# kittiu
	filters = {"disabled": 0}

	if company == parent:
		filters["name"] = get_root_of("Department")
	elif company:
		filters["parent_department"] = parent
		filters["company"] = company
	else:
		filters["parent_department"] = parent
	# kittiu: Chage order_by name to custom_order
	return frappe.get_all("Department", fields=fields, filters=filters, order_by="custom_order, name")

