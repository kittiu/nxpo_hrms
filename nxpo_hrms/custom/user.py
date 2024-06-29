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

	roles = sorted([role.get("name") for role in roles])
	# Remove "User: " roles
	roles = filter(lambda r: OWN_ROLE_PREFIX not in r, roles)
	return roles


def create_user_own_role(user, method):
	"""
	For every user in the system, create a role for him/her if not already exists
	This role is used specifically for workflow processing
	"""
	own_role = frappe.db.get_value(
		"Role",
		{"role_name": "{}{}".format(OWN_ROLE_PREFIX, user.name)},
		"role_name"
	)
	if own_role:  # Already exists
		return
	# Create
	own_role = "{}{}".format(OWN_ROLE_PREFIX, user.name)
	role = frappe.get_doc({
		"doctype": "Role",
		"role_name": own_role,
	})
	role.insert(ignore_permissions=True)
	# Assign
	user.add_roles(role.name)

