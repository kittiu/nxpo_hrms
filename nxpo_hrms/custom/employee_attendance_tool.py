import datetime

import frappe
from hrms.hr.doctype.employee_attendance_tool.employee_attendance_tool import _get_unmarked_attendance


@frappe.whitelist()
def get_employees(
	date: str | datetime.date,
	department: str | None = None,
	branch: str | None = None,
	company: str | None = None,
) -> dict[str, list]:
	filters = {"status": "Active", "date_of_joining": ["<=", date]}

	for field, value in {"department": department, "branch": branch, "company": company}.items():
		if value:
			filters[field] = value

	employee_list = frappe.get_list(
		"Employee", fields=["employee", "employee_name"], filters=filters, order_by="employee_name"
	)
	attendance_list = frappe.get_list(
		"Attendance",
		# fields=["employee", "employee_name", "status"],
		fields=["employee", "employee_name", "status", "custom_work_from_anywhere"],
		filters={
			"attendance_date": date,
			"docstatus": 1,
		},
		order_by="employee_name",
	)

	unmarked_attendance = _get_unmarked_attendance(employee_list, attendance_list)

	return {"marked": attendance_list, "unmarked": unmarked_attendance}
