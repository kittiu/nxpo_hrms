import frappe

def has_app_permission():
    user = frappe.session.user

    if user == "Administrator":
        return True

    roles_to_check = {"Employee"}
    user_roles = frappe.get_roles(user)

    return not roles_to_check.isdisjoint(user_roles)


def remove_app_permission():
    return False