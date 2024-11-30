import frappe
from frappe import _
from frappe.utils import get_link_to_form
from .user import OWN_ROLE_PREFIX
from thai_leave.custom.leave_application import LeaveApplicationThai
from hrms.hr.doctype.leave_application.leave_application import get_approved_leaves_for_period, get_holidays, date_diff, getdate


class LeaveApplicationNXPO(LeaveApplicationThai):
	
    def validate_applicable_after(self):
        # Override because, the applicable after is not just working day
        # Skip validation if syncing with TigerSoft
        if frappe.flags.sync_tigersoft:
            return
        # --
        if self.leave_type:
            leave_type = frappe.get_doc("Leave Type", self.leave_type)
            if leave_type.applicable_after > 0:
                date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")
                number_of_days = date_diff(getdate(self.from_date), date_of_joining)
                if number_of_days >= 0:
                    if number_of_days < leave_type.applicable_after:
                        frappe.throw(
                            _("{0} applicable after {1} working days").format(
                                self.leave_type, leave_type.applicable_after
                            )
                        )

    def validate_dates_across_allocation(self):
        # Skip validation if syncing with TigerSoft
        if frappe.flags.sync_tigersoft:
            return
        super().validate_dates_across_allocation()

    def validate_leave_overlap(self):
        # Skip validation if syncing with TigerSoft
        if frappe.flags.sync_tigersoft:
            return
        super().validate_leave_overlap()

    def show_insufficient_balance_message(self, leave_balance_for_consumption: float) -> None:
        # Skip validation if syncing with TigerSoft
        if frappe.flags.sync_tigersoft:
            return
        super().show_insufficient_balance_message(leave_balance_for_consumption)


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
    if not doc.custom_approver and not frappe.flags.sync_tigersoft:
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
    approver = ""
    if doc.custom_approver and not frappe.flags.sync_tigersoft:
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
