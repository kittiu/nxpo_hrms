import frappe

@frappe.whitelist()
def get_all_roles():
	"""return all roles"""
	active_domains = frappe.get_active_domains()

	roles = frappe.get_all(
		"Role",
		filters={
			"name": ("not in", frappe.permissions.AUTOMATIC_ROLES),
			"name": ("not like", "WF%"),  # Override
			"disabled": 0,
		},
		or_filters={"ifnull(restrict_to_domain, '')": "", "restrict_to_domain": ("in", active_domains)},
		order_by="name",
	)

	return sorted([role.get("name") for role in roles])
