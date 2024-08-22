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
                    "fieldname": "custom_house_no",
                    "fieldtype": "Data",
                    "label": "House No.",
                    "width": 0
                },
                {
                    "fieldname": "custom_house_no",
                    "fieldtype": "Data",
                    "label": "House No.",
                    "width": 0
                },
                {
                    "fieldname": "custom_street",
                    "fieldtype": "Data",
                    "label": 'Street',
                    "width": 0
                },
                {
                    "fieldname": "custom_subdistrict",
                    "fieldtype": "Data",
                    "label": 'Subdistrict',
                    "width": 0
                },
                {
                    "fieldname": "custom_district",
                    "fieldtype": "Data",
                    "label": 'District',
                    "width": 0
                },
                {
                    "fieldname": "custom_province",
                    "fieldtype": "Data",
                    "label": 'Province',
                    "width": 0
                },
                {
                    "fieldname": "custom_zip_code",
                    "fieldtype": "Data",
                    "label": 'ZIP Code',
                    "width": 0
                },
                {
                    "fieldname": "custom_directorate",
                    "fieldtype": "Data",
                    "label": 'Directorate',
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
    data2 = []

    data_res = []

    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""select 
                '401N' as tax_type,
                c.tax_id,
                row_number() over(order by a.employee) as idx,
                a.employee,
                replace(e.custom_citizen_id, '-', '') as citizen_id,
                e.custom_prefix as prefix,
                e.first_name,
                e.last_name,
                e.custom_directorate,
                a.pay_amount,
                a.deduct_amount,
                '1' as tax_cond,
                e.custom_house_no,
                e.custom_street,
                e.custom_subdistrict,
                e.custom_district,
                e.custom_province,
                e.custom_zip_code,
                a.salary_component,
                a.ss_id
            from
            (select 
                ss.name as ss_id,
                ss.company,
                ss.employee,
                sum(round(ss.gross_pay, 2)) as pay_amount,
                sum(round(sd.amount, 2)) as deduct_amount,
                sd.salary_component
            from `tabSalary Slip` ss
                join `tabSalary Detail` sd on sd.parent = ss.name
                join `tabSalary Component` sc
                    on sc.name = sd.salary_component
                    and sc.is_income_tax_component = true and sc.name != 'ภาษีเงินชดเชย'
            where ss.docstatus = %(docstatus)s
                and posting_date >= %(from_date)s and posting_date <= %(to_date)s
                and ss.company = %(company)s
            group by ss.company, ss.employee
            order by ss.employee) a

            join `tabCompany` c on c.name = a.company
            join `tabPayroll Period` p on p.name = %(payroll_period)s
            join `tabEmployee` e on e.name = a.employee 

            {conditions}

        """,
        filters,
        as_dict=True,
    )
    data = query_data
    
    for row in data:
        print('ss_id', row['ss_id'])
        print('salary_component', row['salary_component'])
        data_res.append(row)


    query_data_2 = frappe.db.sql(
        f"""select 
                '401N' as tax_type,
                c.tax_id,
                row_number() over(order by a.employee) as idx,
                a.employee,
                replace(e.custom_citizen_id, '-', '') as citizen_id,
                e.custom_prefix as prefix,
                e.first_name,
                e.last_name,
                e.custom_directorate,
                a.pay_amount,
                a.deduct_amount,
                '2' as tax_cond,
                e.custom_house_no,
                e.custom_street,
                e.custom_subdistrict,
                e.custom_district,
                e.custom_province,
                e.custom_zip_code,
                a.salary_component,
                a.ss_id
            from
            (select 
                ss.name as ss_id,
                ss.company,
                ss.employee,
                sum(round(ss.gross_pay, 2)) as pay_amount,
                sum(round(sd.amount, 2)) as deduct_amount,
                sd.salary_component
            from `tabSalary Slip` ss
                join `tabSalary Detail` sd on sd.parent = ss.name
                join `tabSalary Component` sc
                    on sc.name = sd.salary_component
                    and sc.is_income_tax_component = true and sc.name = 'ภาษีเงินชดเชย'
            where ss.docstatus = %(docstatus)s
                and posting_date >= %(from_date)s and posting_date <= %(to_date)s
                and ss.company = %(company)s
            group by ss.company, ss.employee
            order by ss.employee) a

            join `tabCompany` c on c.name = a.company
            join `tabPayroll Period` p on p.name = %(payroll_period)s
            join `tabEmployee` e on e.name = a.employee 

            {conditions}
        """,
        filters,
        as_dict=True,
    )


    data2 = query_data_2

    for row2 in data2:
        data_res.append(row2)
        
    return data_res

def get_conditions(filters):
    conditions = []

    # Directorate filter when pmu_or_nxpo is None
    if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
        conditions.append("e.custom_directorate = %(directorate)s")
    
    # PMU or NXPO conditions
    pmu_conditions = [
        "e.custom_directorate = 'บพข. - N'",
        "e.custom_directorate = 'บพค. - N'",
        "e.custom_directorate = 'บพท. - N'"
    ]

    pmu_or_nxpo = filters.get("pmu_or_nxpo")
    if pmu_or_nxpo == 'pmu':
        conditions.append(f"({' or '.join(pmu_conditions)})")
    elif pmu_or_nxpo == 'nxpo':
        conditions.append(f"NOT ({' or '.join(pmu_conditions)})")

    # Build the WHERE clause
    return "WHERE " + " AND ".join(conditions) if conditions else ""