import frappe


OWN_ROLE_PREFIX = "User: "

@frappe.whitelist()
def get_all_roles():
	"""return all roles"""
	active_domains = frappe.get_active_domains()

	roles = frappe.get_all(
		"Role",
		filters={
			"name": ("not in", frappe.permissions.AUTOMATIC_ROLES),
			"disabled": 0,
		},
		or_filters={"ifnull(restrict_to_domain, '')": "", "restrict_to_domain": ("in", active_domains)},
		order_by="name",
	)

	# Remove "WF" and "User: " roles
	roles = sorted([role.get("name") for role in roles])
	roles = filter(lambda r: "WF" not in r, roles)
	roles = filter(lambda r: "{}%".format(OWN_ROLE_PREFIX) not in r, roles)
	return roles


def reset_user_own_role(user, method):
	"""
	For every user in the system, create a role for him/her
	This role is used specifically for workflow processing
	"""
	# Check if this user already has a valid role with correct naming
	# Find any UID role with OWN_ROLE_PREFIX for this user
	# TODO
	own_role = frappe.db.get_value(
		"Has Role",
		{
			"parenttype": "User",
			"parent": user.name,
			"role": ["like", "{}%".format(OWN_ROLE_PREFIX)],
		},
		"role"
	)
	if own_role == "{}{}".format(OWN_ROLE_PREFIX, user.name):
		return

	# If existing but incorrect name, continue to reset
	# Delete
	if own_role:
		role = frappe.get_doc("Role", own_role)
		role.remove_roles()
		role.delete()
	# Create
	new_own_role = "{}{}".format(OWN_ROLE_PREFIX, user.name)
	role = frappe.get_doc({
		"doctype": "Role",
		"role_name": new_own_role,
	})
	role.insert(ignore_permissions=True)
	# Assign
	user.add_roles(role.name)

