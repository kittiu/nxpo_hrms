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
                "fieldname": "name",
                "fieldtype": "Link",
                "label": "ID",
                "options": "Employee Tailor Tracker",
                "width": 0
            },
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
                "fieldname": "custom_directorate",
                "fieldtype": "Data",
                "label": "Directorate",
                "width": 0
            },
            {
                "fieldname": "round",
                "fieldtype": "Int",
                "label": "Round",
                "width": 0
            },
            {
                "fieldname": "time",
                "fieldtype": "Int",
                "label": "Time",
                "width": 0
            },
            {
                "fieldname": "latest_tailor_date",
                "fieldtype": "Date",
                "label": "Latest Tailor Date",
                "width": 0
            },
            {
                "fieldname": "remaining_months",
                "fieldtype": "Int",
                "label": "Remaining Months",
                "width": 0
            },
            {
                "fieldname": "end_date",
                "fieldtype": "Date",
                "label": "End Date",
                "width": 0
            },
            {
                "fieldname": "balance",
                "fieldtype": "Currency",
                "label": "Balance",
                "width": 0
            }
    ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""select 
                a.name,
                a.employee,
                a.employee_name,
                a.round,
                a.time,
                b.latest_tailor_date,
                timestampdiff(month, current_date,  a.end_date) remaining_months,
                a.end_date,
                a.balance,
                emp.custom_directorate
            from `tabEmployee Tailor Tracker` a
            join
            (select employee, max(tailor_date) latest_tailor_date
            from `tabEmployee Tailor Tracker`
            group by employee) b
            on a.employee = b.employee and a.tailor_date = b.latest_tailor_date
            join `tabEmployee` emp on emp.name = a.employee
            {conditions}
            order by a.employee """,
        filters,
        as_dict=True,
    )
    data = query_data

    return data

def get_conditions(filters):
    conditions = []

    # Directorate filter when pmu_or_nxpo is None
    if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
        conditions.append("emp.custom_directorate = %(directorate)s")
    
    # PMU or NXPO conditions
    pmu_conditions = [
        "emp.custom_directorate = 'บพข. - N'",
        "emp.custom_directorate = 'บพค. - N'",
        "emp.custom_directorate = 'บพท. - N'"
    ]

    pmu_or_nxpo = filters.get("pmu_or_nxpo")
    if pmu_or_nxpo == 'pmu':
        conditions.append(f"({' or '.join(pmu_conditions)})")
    elif pmu_or_nxpo == 'nxpo':
        conditions.append(f"NOT ({' or '.join(pmu_conditions)})")

    # Build the WHERE clause
    return "WHERE " + " AND ".join(conditions) if conditions else ""