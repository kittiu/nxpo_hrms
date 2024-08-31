# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data

def get_columns(filters):
    columns = [
            {
                "fieldname": "employee",
                "fieldtype": "Data",
                "label": "Employee Code",
                "width": 0
            },
            {
                "fieldname": "employee_name",
                "fieldtype": "Data",
                "label": "Employee Name",
                "width": 0
            },
            {
                "fieldname": "department",
                "fieldtype": "Data",
                "label": "Department",
                "width": 0
            },
            {
                "fieldname": "attendance_date",
                "fieldtype": "Date",
                "label": "Attendance Date",
                "width": 0
            },
            {
                "fieldname": "status",
                "fieldtype": "Data",
                "label": "Status",
                "width": 0
            },
            {
                "fieldname": "custom_work_from_anywhere",
                "fieldtype": "Check",
                "label": "Work From Anywhere",
                "width": 0
            },
            {
                "fieldname": "wfa_id",
                "fieldtype": "Data",
                "label": "WFA Requests",
                "width": 0
            },
            {
                "fieldname": "type",
                "fieldtype": "Data",
                "label": "Type",
                "width": 0
            },
            {
                "fieldname": "development",
                "fieldtype": "Data",
                "label": "Development",
                "width": 0
            },
    ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""
            select
                emp.employee as employee,
                atd.employee_name,
                emp.department,
                atd.attendance_date,
                atd.status,
                atd.custom_work_from_anywhere,
                wfa.type,
                wfa.development,
                wfa.name as wfa_id
            from `tabAttendance` atd
            left join `tabAttendance Request` atdr on atd.attendance_request = atdr.name
            left join `tabWFA Request` wfa on atdr.custom_wfa_request = wfa.name
            left join `tabEmployee` emp on atd.employee = emp.name
            where atd.company = %(company)s 
                AND atd.attendance_date >= %(from_date)s 
                AND atd.attendance_date <= %(to_date)s 
                {('AND ' + conditions) if conditions else ''}
        """,
        filters,
        as_dict=True,
    )
    data = query_data

    return data

def get_conditions(filters):
    conditions = []

    if filters.get("atd_status"):
        conditions.append("atd.status = %(atd_status)s")
    
    if filters.get("is_wfa"):
        conditions.append("atd.custom_work_from_anywhere = %(is_wfa)s")
    
    if filters.get("employee_f"):
        conditions.append("atd.employee = %(employee_f)s")

    # Combine conditions into a single string
    return " AND ".join(conditions)