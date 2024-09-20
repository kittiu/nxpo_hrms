# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from dateutil.relativedelta import relativedelta



def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data

def get_columns(filters):
    columns = [
            {
                "fieldname": "tax_type",
                "fieldtype": "Data",
                "label": "เงินได้ตามมาตรา",
                "width": 0
            },
            {
                "fieldname": "tax_id",
                "fieldtype": "Data",
                "label": "เลขทะเบียนนิติบุคคล",
                "width": 0
            },
            {
                "fieldname": "idx",
                "fieldtype": "Int",
                "label": "ลำดับที่",
                "width": 0
            },
            {
                "fieldname": "employee",
                "fieldtype": "Link",
                "label": "เลขที่พนักงาน",
                "options": "Employee",
                "width": 0
            },
            {
                "fieldname": "citizen_id",
                "fieldtype": "Data",
                "label": "เลขประจำตัวผู้เสียภาษี",
                "width": 0
            },
            {
                "fieldname": "prefix",
                "fieldtype": "Data",
                "label": "คำนำหน้าชื่อ",
                "width": 0
            },
            {
                "fieldname": "first_name",
                "fieldtype": "Data",
                "label": "ชื่อ",
                "width": 0
            },
            {
                "fieldname": "last_name",
                "fieldtype": "Data",
                "label": "นามสกุล",
                "width": 0
            },
            {
                "fieldname": "directorate",
                "fieldtype": "Data",
                "label": 'ชื่อกลุ่ม/ฝ่าย',
                "width": 0
            },
            {
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "label": "วันเดือนปีที่จ่าย",
                "width": 0
            },
            {
                "fieldname": "pay_amount",
                "fieldtype": "Currency",
                "label": "จำนวนเงินที่จ่าย",
                "width": 0
            },
            {
                "fieldname": "deduct_amount",
                "fieldtype": "Currency",
                "label": "จำนวนเงินภาษีที่หัก",
                "width": 0
            },
            {
                "fieldname": "tax_cond",
                "fieldtype": "Data",
                "label": "เงื่อนไขการหัก",
                "width": 0
              }
    ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""select 
                '401N' as tax_type,
                c.tax_id,
                row_number() over(order by emp.name) as idx,
                emp.name as employee,
                replace(emp.custom_citizen_id, '-', '') as citizen_id,
                emp.custom_prefix as prefix,
                emp.first_name,
                emp.last_name,
                emp.custom_directorate AS directorate,
                ss.posting_date,
                round(ss.gross_pay, 2) as pay_amount,
                round(sd.amount, 2) as deduct_amount,
                sd.salary_component
            from `tabSalary Slip` ss join `tabEmployee` emp on ss.employee = emp.name
                join `tabCompany` c on ss.company = c.name
                join `tabSalary Detail` sd on sd.parent = ss.name
                join `tabSalary Component` sc
                    on sc.name = sd.salary_component
                    and sc.is_income_tax_component = true
            where posting_date >= %(from_date)s and posting_date <= %(to_date)s
                and ss.docstatus = %(docstatus)s
                and emp.company = %(company)s {conditions}
            order by emp.name """,
        filters,
        as_dict=True,
    )
    data = query_data

    for row in data:
        if 'เงินชดเชย' in row['salary_component']:
            row['tax_cond'] = 2
        else:
            row['tax_cond'] = 1

    return data

def get_conditions(filters):
    conditions = ""

    if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
        conditions += f"and emp.custom_directorate = %(directorate)s"
    
    pmu_conditions = [
        "emp.custom_directorate = 'บพข. - N'",
        "emp.custom_directorate = 'บพค. - N'",
        "emp.custom_directorate = 'บพท. - N'"
    ]

    if filters.get("pmu_or_nxpo") == 'pmu':
        conditions += f"and ({' or '.join(pmu_conditions)})"
    elif filters.get("pmu_or_nxpo") == 'nxpo':
        conditions += f"and not ({' or '.join(pmu_conditions)})"
    

    return conditions