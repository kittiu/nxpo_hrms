# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe.utils.nestedset import get_root_of


@frappe.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	fields = ["name as value", "is_group as expandable"]
	filters = {}

	if company == parent:
		filters["name"] = get_root_of("Department")
	elif company:
		filters["parent_department"] = parent
		filters["company"] = company
	else:
		filters["parent_department"] = parent
	# kittiu: Chage order_by namt -> custom_order
	return frappe.get_all("Department", fields=fields, filters=filters, order_by="custom_order, name")

