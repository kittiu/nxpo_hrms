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


def compute_approvers(doc, method):
    doc.custom_approvers = []  # Reset table
    for (position, approver) in get_leave_approvers(doc):
        doc.append(
            "custom_approvers",
            {
                "position": position,
                "approver_role": approver,
            }
        )
    if not doc.custom_approvers:
        frappe.throw(_("Approvers not found for {}: {}").format(
            get_link_to_form("Employee", doc.employee),
            doc.employee_name
        ))
    doc.custom_approver_count = len(doc.custom_approvers)


def get_leave_approvers(leave):
    """
    For leave type = ลาพัก, approvers are
    1. Employee's Department Chief
    2. Employee's Directorate Assistant
    3. Employee's Directorate Chief
    If Employee do not have Directorate or leave type = อื่นๆ then
    For leave type = อื่นๆ, approvers are
    1. Employee's Leave Approver
    """
    role_dept_chief = None
    role_dir_chief = None
    role_dir_assist = None
    role_leave_approver = None
    employee = frappe.get_doc("Employee", leave.employee)
    # ลาพักผ่อน
    if leave.leave_type == "ลาพักผ่อน":
        if employee.department:
            department = frappe.get_doc("Department", employee.department)
            role_dept_chief = get_employee_role(department.custom_chief, department.custom_chief_name)
        if employee.custom_directorate:
            directorate = frappe.get_doc("Department", employee.custom_directorate)
            role_dir_chief = get_employee_role(directorate.custom_chief, directorate.custom_chief_name)
            role_dir_assist = get_employee_role(directorate.custom_assistant, directorate.custom_assistant_name)
        else: # for CEO only, use leave approver
            role_leave_approver = "{}{}".format(OWN_ROLE_PREFIX, employee.leave_approver)
    # Others
    else:
        if not employee.leave_approver:
            frappe.throw(_("No Leave Approver setup for {}: {}").format(
                get_link_to_form("Employee", employee.name),
                employee.employee_name
            ))
        role_leave_approver = "{}{}".format(OWN_ROLE_PREFIX, employee.leave_approver)
    # Set approvers table
    approvers = [
        ("ผู้อำนวยการฝ่ายงาน", role_dept_chief),
        ("ผู้ช่วยผู้อำนวยการกลุ่มงาน", role_dir_assist),
        ("ผู้อำนวยการกลุ่มงาน", role_dir_chief),
        ("ผู้อนุมัติการลาของพนักงาน", role_leave_approver)
    ]
    approvers = filter(lambda x: x[1], approvers)
    return approvers


def share_to_approvers(doc, method):
    # Share with approvers to allow access
    approvers = [x.approver_role.replace(OWN_ROLE_PREFIX, "") for x in doc.custom_approvers]
    shared_users = [x.user for x in frappe.share.get_users(doc.doctype, doc.name)]
    # For shared users not in approvers list, remove share
    for user in (set(shared_users) - set(approvers)):
        frappe.share.remove(
            doc.doctype,
            doc.name,
            user,
            flags={"ignore_share_permission": True}
        )
    # For approvers not in shared users list, add share
    for user in (set(approvers) - set(shared_users)):
        frappe.share.add_docshare(
            doc.doctype,
            doc.name,
            user,
            read=1, write=1, submit=1, notify=0,
            flags={"ignore_share_permission": True}
        )

