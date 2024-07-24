import frappe
from frappe import _
from frappe.utils import get_link_to_form
from .user import OWN_ROLE_PREFIX


def get_employee_role(employee, employee_name):
    if employee:
        user = frappe.db.get_value("Employee", employee, "user_id")
        if not user:
            frappe.throw(_("{}: {} has no User ID").format(
                get_link_to_form("Employee", employee),
                employee_name
            ))
        return "{}{}".format(OWN_ROLE_PREFIX, user)
    return


def compute_approver(doc, method):
    doc.custom_approver = get_leave_approver_role(doc)
    if not doc.custom_approver:
        frappe.throw(_("Approver not found for {}: {}").format(
            get_link_to_form("Employee", doc.employee),
            doc.employee_name
        ))


def get_leave_approver_role(leave):
    """
    * If Employee's Leave Approver is set, use it as approver role
    * If Employee has Department, use Department Chief as approver role
    * If Employee has Department, but is Department Chief himself, use Directorate Assistant as approver role
    * If Employee has only Directorate, use Directorate Chief as approver role
    * Else return None
    """
    employee = frappe.get_doc("Employee", leave.employee)
    if employee.leave_approver:
        role_leave_approver = "{}{}".format(OWN_ROLE_PREFIX, employee.leave_approver)
        return role_leave_approver
    # Employee has Department
    if employee.department:
        department = frappe.get_doc("Department", employee.department)
        if department.custom_chief != leave.employee:
            return get_employee_role(department.custom_chief, department.custom_chief_name)
        directorate = frappe.get_doc("Department", employee.custom_directorate)
        return get_employee_role(directorate.custom_assistant, directorate.custom_assistant_name)
    # Employee has only Directorate
    if employee.custom_directorate:
        directorate = frappe.get_doc("Department", employee.custom_directorate)
        if directorate.custom_chief != leave.employee:
            return get_employee_role(directorate.custom_chief, directorate.custom_chief_name)
    return None


def share_to_approver(doc, method):
    # Share with approvers to allow access
    approver = doc.custom_approver.replace(OWN_ROLE_PREFIX, "")
    shared_users = [x.user for x in frappe.share.get_users(doc.doctype, doc.name)]
    # For shared users not in approvers list, remove share
    for user in (set(shared_users) - set([approver])):
        frappe.share.remove(
            doc.doctype,
            doc.name,
            user,
            flags={"ignore_share_permission": True}
        )
    # For approvers not in shared users list, add share
    for user in (set([approver]) - set(shared_users)):
        frappe.share.add_docshare(
            doc.doctype,
            doc.name,
            user,
            read=1, write=1, submit=1, notify=0,
            flags={"ignore_share_permission": True}
        )
