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
                "fieldname": "employee_code",
                "fieldtype": "Data",
                "label": "รหัส",
                "width": 0
            },
            {
                "fieldname": "employee_name",
                "fieldtype": "Data",
                "label": "ชื่อ-นามสกุล",
                "width": 0
            },
            {
                "fieldname": "designation",
                "fieldtype": "Data",
                "label": "ตำแหน่ง",
                "width": 0
            },
            {
                "fieldname": "directorate",
                "fieldtype": "Data",
                "label": "กลุ่ม",
                "width": 0
            },
            {
                "fieldname": "department",
                "fieldtype": "Data",
                "label": "ฝ่าย",
                "width": 0
            },
            {
                "fieldname": "date_of_birth",
                "fieldtype": "Date",
                "label": "วันเกิด",
                "width": 0
            },
            {
                "fieldname": "age",
                "fieldtype": "Data",
                "label": "อายุ",
                "width": 0
            },
            {
                "fieldname": "date_of_joining",
                "fieldtype": "Date",
                "label": "วันที่เริ่มงาน",
                "width": 0
            },
            {
                "fieldname": "exp",
                "fieldtype": "Data",
                "label": "อายุงาน",
                "width": 0
            },
            {
                "fieldname": "received_date",
                "fieldtype": "Data",
                "label": "ปีที่เคยได้รับเครื่องราช",
                "width": 0
            },
            {
                "fieldname": "received_royal_decoration",
                "fieldtype": "Data",
                "label": "เครื่องราชฯที่เคยได้รับ",
                "width": 0
            },
            {
                "fieldname": "remarks",
                "fieldtype": "Data",
                "label": "หมายเหตุ",
                "width": 0
            }
        ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)
    query_data = frappe.db.sql(
        f"""select 
                emp.name as employee_code,
                emp.employee_name,
                emp.designation,
                (select department_name from tabDepartment where name = emp.custom_directorate) as directorate,
                (select department_name from tabDepartment where name = emp.department) as department,
                emp.date_of_birth,
                CONCAT(
                TIMESTAMPDIFF(YEAR, emp.date_of_birth, CURDATE()), ' ปี ',
                TIMESTAMPDIFF(MONTH, emp.date_of_birth, CURDATE()) %% 12, ' เดือน ',
                DATEDIFF(
                CURDATE(),
                DATE_ADD(
                DATE_ADD(emp.date_of_birth, INTERVAL TIMESTAMPDIFF(YEAR, emp.date_of_birth, CURDATE()) YEAR),
                INTERVAL TIMESTAMPDIFF(MONTH, emp.date_of_birth, CURDATE()) %% 12 MONTH
                )
                ), ' วัน') as age,
                emp.date_of_joining,
                REPLACE(REPLACE(REPLACE(emp.custom_experience_ytd, 'Years', 'ปี'), 'Months', 'เดือน'), 'Days', 'วัน') as exp,
                YEAR(erd.received_date) as received_date,
                erd.received_royal_decoration,
                erd.remarks
            from `tabEmployee Royal Decoration` erd
            join `tabEmployee` emp on emp.name = erd.employee
            {conditions}
            order by YEAR(erd.received_date) desc""",
        filters,
        as_dict=True,
    )

    data = query_data
    return data

def get_conditions(filters):
    conditions = []

    if filters.get("year"):
        conditions.append("YEAR(erd.received_date) <= %(year)s")
    if filters.get("employee"):
        conditions.append("emp.name = %(employee)s")

    if conditions:
        return "WHERE " + " AND ".join(conditions)
    else:
        return ""
