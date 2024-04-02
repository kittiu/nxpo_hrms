# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.desk.form import assign_to
from frappe.utils import add_days, flt, unique

from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday


def remove_task_from_activities(doc, method=None):
    # remove the task if linked before submitting the form
    activities = (
        doc.custom_promotion_activities
        if doc.doctype == "Employee Promotion"
        else doc.custom_transfer_activities
    )
    if doc.amended_from:
        for activity in activities:
            activity.task = ""


def create_project(doc, method=None):
    # create the project for the given employee transition
    project_name = "{} : {}".format(doc.name, doc.employee_name)
    action_date = (
        doc.promotion_date
        if doc.doctype == "Employee Promotion"
        else doc.transfer_date
    )

    project = frappe.get_doc(
        {
            "doctype": "Project",
            "project_name": project_name,
            "expected_start_date": action_date,
            "department": doc.department,
            "company": doc.company,
        }
    ).insert(ignore_permissions=True, ignore_mandatory=True)

    doc.db_set("custom_project", project.name)
    doc.db_set("custom_transition_status", "Pending")
    doc.reload()
    create_task_and_notify_user(doc)


def create_task_and_notify_user(doc, method=None):
    # create the task for the given project and assign to the concerned person
    holiday_list = get_holiday_list(doc)
    activities = (
        doc.custom_promotion_activities
        if doc.doctype == "Employee Promotion"
        else doc.custom_transfer_activities
    )
    for activity in activities:
        if activity.task:
            continue

        dates = get_task_dates(doc, activity, holiday_list)

        task = frappe.get_doc(
            {
                "doctype": "Task",
                "project": doc.custom_project,
                "subject": activity.activity_name + " : " + doc.employee_name,
                "description": activity.description,
                "department": doc.department,
                "company": doc.company,
                "task_weight": activity.task_weight,
                "exp_start_date": dates[0],
                "exp_end_date": dates[1],
            }
        ).insert(ignore_permissions=True)
        activity.db_set("task", task.name)

        users = [activity.user] if activity.user else []
        if activity.role:
            user_list = frappe.db.sql_list(
                """
                SELECT
                    DISTINCT(has_role.parent)
                FROM
                    `tabHas Role` has_role
                        LEFT JOIN `tabUser` user
                            ON has_role.parent = user.name
                WHERE
                    has_role.parenttype = 'User'
                        AND user.enabled = 1
                        AND has_role.role = %s
            """,
                activity.role,
            )
            users = unique(users + user_list)

            if "Administrator" in users:
                users.remove("Administrator")

        # assign the task the users
        if users:
            assign_task_to_users(doc, task, users)


def get_holiday_list(doc):
    if doc.employee:
        return get_holiday_list_for_employee(doc.employee)
    else:
        if not doc.holiday_list:
            frappe.throw(_("Please set the Holiday List."), frappe.MandatoryError)
        else:
            return doc.holiday_list


def get_task_dates(doc, activity, holiday_list):
    start_date = end_date = None
    action_date = (
        doc.promotion_date
        if doc.doctype == "Employee Promotion"
        else doc.transfer_date
    )
    if activity.begin_on is not None:
        start_date = add_days(action_date, activity.begin_on)
        start_date = update_if_holiday(start_date, holiday_list)

        if activity.duration is not None:
            end_date = add_days(action_date, activity.begin_on + activity.duration)
            end_date = update_if_holiday(end_date, holiday_list)

    return [start_date, end_date]


def update_if_holiday(date, holiday_list):
    while is_holiday(holiday_list, date):
        date = add_days(date, 1)
    return date


def assign_task_to_users(doc, task, users):
    for user in users:
        args = {
            "assign_to": [user],
            "doctype": task.doctype,
            "name": task.name,
            "description": task.description or task.subject,
            "notify": doc.custom_notify_users_by_email,
        }
        assign_to.add(args)


def delete_project_task(doc, method=None):
    # delete task project
    project = doc.custom_project
    for task in frappe.get_all("Task", filters={"project": project}):
        frappe.delete_doc("Task", task.name, force=1)
    frappe.delete_doc("Project", project, force=1)
    doc.db_set("custom_project", "")
    activities = (
        doc.custom_promotion_activities
        if doc.doctype == "Employee Promotion"
        else doc.custom_transfer_activities
    )    
    for activity in activities:
        activity.db_set("task", "")

    frappe.msgprint(
        _("Linked Project {} and Tasks deleted.").format(project), alert=True, indicator="blue"
    )


@frappe.whitelist()
def get_transition_details(parent, parenttype):
    return frappe.get_all(
        "Employee Transition Activity",
        fields=[
            "activity_name",
            "role",
            "user",
            "description",
            "task_weight",
            "begin_on",
            "duration",
        ],
        filters={"parent": parent, "parenttype": parenttype},
        order_by="idx",
    )


def update_employee_transition_status(project, event=None):
    employee_promotion = frappe.db.exists("Employee Promotion", {"custom_project": project.name})
    employee_transfer = frappe.db.exists("Employee Transfer", {"custom_project": project.name})

    if not (employee_promotion or employee_transfer):
        return

    status = "Pending"
    if flt(project.percent_complete) > 0.0 and flt(project.percent_complete) < 100.0:
        status = "In Process"
    elif flt(project.percent_complete) == 100.0:
        status = "Completed"

    if employee_promotion:
        frappe.db.set_value("Employee Promotion", employee_promotion, "custom_transition_status", status)
    elif employee_transfer:
        frappe.db.set_value("Employee Transfer", employee_transfer, "custom_transition_status", status)


def update_task(task, method=None):
    if task.project and not task.flags.from_project:
        update_employee_transition_status(frappe.get_cached_doc("Project", task.project))
