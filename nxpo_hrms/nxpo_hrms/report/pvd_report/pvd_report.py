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
            "fieldname": "idx",
            "fieldtype": "Data",
            "label": "\u0e25\u0e33\u0e14\u0e31\u0e1a\u0e17\u0e35\u0e48",
            "width": 0
        },
        {
            "fieldname": "employee",
            "fieldtype": "Data",
            "label": "\u0e23\u0e2b\u0e31\u0e2a\u0e1e\u0e19\u0e31\u0e01\u0e07\u0e32\u0e19",
            "options": "",
            "width": 0
        },
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": "\u0e0a\u0e37\u0e48\u0e2d-\u0e19\u0e32\u0e21\u0e2a\u0e01\u0e38\u0e25",
            "width": 0
        },
        {
            "fieldname": "salary",
            "fieldtype": "Currency",
            "label": "\u0e40\u0e07\u0e34\u0e19\u0e40\u0e14\u0e37\u0e2d\u0e19",
            "width": 0
        },
        {
            "fieldname": "back_salary",
            "fieldtype": "Currency",
            "label": "\u0e15\u0e01\u0e40\u0e1a\u0e34\u0e01",
            "width": 0
        },
        {
            "fieldname": "pvd_start_date",
            "fieldtype": "Date",
            "label": "\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e40\u0e23\u0e34\u0e48\u0e21\u0e04\u0e34\u0e14\u0e2d\u0e32\u0e22\u0e38\u0e01\u0e2d\u0e07\u0e17\u0e38\u0e19",
            "width": 0
        },
        {
            "fieldname": "pvd_emp",
            "fieldtype": "Currency",
            "label": "\u0e1e\u0e19\u0e31\u0e01\u0e07\u0e32\u0e19\u0e2a\u0e30\u0e2a\u0e21",
            "width": 0
        },
        {
            "fieldname": "pvd_emp_percent",
            "fieldtype": "Int",
            "label": "% \u0e2a\u0e30\u0e2a\u0e21",
            "width": 0
        },
        {
            "fieldname": "pvd_com",
            "fieldtype": "Currency",
            "label": "\u0e1a\u0e23\u0e34\u0e29\u0e31\u0e17\u0e2a\u0e21\u0e17\u0e1a",
            "width": 0
        },
        {
            "fieldname": "pvd_com_percent",
            "fieldtype": "Int",
            "label": "% \u0e2a\u0e30\u0e2a\u0e21",
            "width": 0
        },
        {
            "fieldname": "pvd_total",
            "fieldtype": "Currency",
            "label": "\u0e23\u0e27\u0e21\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14",
            "width": 0
        },
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "Posting Date",
            "width": 0
        }
	]

	return columns

def get_data(filters):
    data = []

    conditions = get_conditions(filters)
    query_data = frappe.db.sql(
		f"""SELECT
            CONVERT(row_number() OVER (ORDER BY ss.employee), char) AS idx,
            ss.employee,
            emp.employee_name,
            salary.amount AS salary,
            back_salary.amount AS back_salary,
            emp.date_of_joining AS pvd_start_date,
            pvd_emp.amount AS pvd_emp,
            ss.custom_pvd_employee AS pvd_emp_percent,
            pvd_com.amount AS pvd_com,
            ss.custom_pvd_company AS pvd_com_percent,
            COALESCE(pvd_emp.amount, 0) + COALESCE(pvd_com.amount, 0) AS pvd_total,
            ss.posting_date
        FROM `tabSalary Slip` ss
        JOIN `tabEmployee` emp ON ss.employee = emp.name
        LEFT JOIN `tabSalary Detail` salary ON salary.parenttype = 'Salary Slip' 
            AND salary.parentfield = 'earnings' 
            AND salary.parent = ss.name 
            AND salary.salary_component = 'เงินเดือน'
        LEFT JOIN `tabSalary Detail` back_salary ON back_salary.parenttype = 'Salary Slip' 
            AND back_salary.parentfield = 'earnings' 
            AND back_salary.parent = ss.name 
            AND back_salary.salary_component = 'ตกเบิก'
        LEFT JOIN `tabSalary Detail` pvd_emp ON pvd_emp.parenttype = 'Salary Slip' 
            AND pvd_emp.parentfield = 'deductions' 
            AND pvd_emp.parent = ss.name 
            AND pvd_emp.salary_component = 'กองทุนสำรองเลี้ยงชีพ'
        LEFT JOIN `tabSalary Detail` pvd_com ON pvd_com.parenttype = 'Salary Slip' 
            AND pvd_com.parentfield = 'deductions' 
            AND pvd_com.parent = ss.name 
            AND pvd_com.salary_component = 'กองทุนบริษัทสมทบ'
        WHERE ss.docstatus = %(docstatus)s
            AND ss.start_date = %(from_date)s
            AND ss.end_date = %(to_date)s
            AND ss.company = %(company)s {conditions}""",
		filters,
		as_list=1,
	)

    data = query_data
    return data


def get_conditions(filters):
	conditions = ""

	if filters.get("pvd_type"):
		conditions += f"and ss.custom_pvd_type = %(pvd_type)s"

	return conditions