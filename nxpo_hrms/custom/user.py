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
	if own_role:  # Already exists, just make sure user has it
		user.append_roles(own_role)
		return
	# Create
	own_role = "{}{}".format(OWN_ROLE_PREFIX, user.name)
	role = frappe.get_doc({
		"doctype": "Role",
		"role_name": own_role,
	})
	role.insert(ignore_permissions=True)
	# Assign
	user.append_roles(role.name)


def validate_update_role_profile(doc, method):
	"""If user is has role User Admin, make sure he/she cannot change role_profile"""
	if doc.name != frappe.session.user:
		return
	if "User Admin" in frappe.get_roles():
		doc_before_save = doc.get_doc_before_save()
		if doc.role_profile_name != doc_before_save.role_profile_name:
			frappe.throw("User Admin cannot change his/her own Role Profile")
