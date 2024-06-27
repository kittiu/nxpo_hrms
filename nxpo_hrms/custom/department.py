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


def reset_approval_role(doc, method):
	"""
	If Chief and Assistant are not empty, create approval role for this department
	and then assigne Chief and Assistant to this role
	"""
	old_doc = doc.get_doc_before_save()
	if (
		doc.custom_chief == old_doc.custom_chief
	 	and doc.custom_assistant == old_doc.custom_assistant
	):
		return

	# First remove all roles
	roles = [doc.custom_chief_role, doc.custom_assistant_role]
	frappe.db.set_value("Department", doc.name, "custom_chief_role", None)
	frappe.db.set_value("Department", doc.name, "custom_assistant_role", None)
	for role in filter(lambda r: r, roles):
		role = frappe.get_cached_doc("Role", role)
		role.remove_roles()
		role.delete()

	# Create new role for chief / assistant
	roles = [
		(doc.custom_chief, "custom_chief_role"),
		(doc.custom_assistant, "custom_assistant_role"),
	]
	for i, r in enumerate(roles):
		if r[0]:
			role = frappe.get_cached_doc({
				"doctype": "Role",
				"role_name": "WF{}-{}".format(i+1, doc.custom_department_sync_code),
			})
			role.insert(ignore_permissions=True)
			frappe.db.set_value("Department", doc.name, r[1], role.role_name)
	doc.reload()

	# Add role to user
	roles = [
		(doc.custom_chief_role, doc.custom_chief),
		(doc.custom_assistant_role, doc.custom_assistant),
	]
	for r in roles:
		if r[0]:
			employee = frappe.get_cached_doc("Employee", r[1])
			if not employee.user_id:
				frappe.throw(_("User not found for {}: {}").format(
					employee.name, employee.employee_name
				))
			user = frappe.get_cached_doc("User", employee.user_id)
			user.add_roles(doc.custom_chief_role)


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

