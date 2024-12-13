# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime


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
                    "label": "เลขที่",
                    "width": 0
                },
                {
                    "fieldname": "custom_village_building",
                    "fieldtype": "Data",
                    "label": "หมู่บ้าน/อาคาร",
                    "width": 0
                },
                {
                    "fieldname": "custom_soi",
                    "fieldtype": "Data",
                    "label": "ซอย",
                    "width": 0
                },
                {
                    "fieldname": "custom_street",
                    "fieldtype": "Data",
                    "label": "ถนน",
                    "width": 0
                },
                {
                    "fieldname": "custom_subdistrict",
                    "fieldtype": "Data",
                    "label": "แขวง/ตำบล",
                    "width": 0
                },
                {
                    "fieldname": "custom_district",
                    "fieldtype": "Data",
                    "label": "เขต/อำเภอ",
                    "width": 0
                },
                {
                    "fieldname": "custom_province",
                    "fieldtype": "Data",
                    "label": "จังหวัด",
                    "width": 0
                },
                {
                    "fieldname": "custom_zip_code",
                    "fieldtype": "Data",
                    "label": "รหัสไปรษณีย์",
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
                e.custom_village_building,
                e.custom_soi,
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
        # Case opening amount
        ss_name = frappe.get_all(
            "Salary Slip", {
                "employee": row["employee"],
                "posting_date": ["<=", filters["to_date"]],
                "docstatus": 1,
            },
            order_by="posting_date desc",
            pluck="name",
            limit=1
        )
        ss = frappe.get_cached_doc("Salary Slip", ss_name[0])
        row["pay_amount"] += ss.get_opening_for("taxable_earnings_till_date", None, None)
        row["deduct_amount"] += ss.get_opening_for("tax_deducted_till_date", None, None)
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
                e.custom_village_building,
                e.custom_soi,
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
        row2['idx'] = len(data_res) + 1
        data_res.append(row2)

    if filters.get("is_use_ssa"):
        query_ssa = frappe.db.sql(
        """
            SELECT 
                ssa.employee
            FROM 
                `tabSalary Structure Assignment` ssa
            WHERE 
                ssa.taxable_earnings_till_date IS NOT NULL
                AND ssa.tax_deducted_till_date IS NOT NULL
            GROUP BY 
                ssa.employee
        """,
            as_dict=True,
        )
        data_ssa = query_ssa
        
        # Convert the lists into sets for efficient comparison
        employees_set = set([row['employee'] for row in data_res])
        ssa_set = set([row['employee'] for row in data_ssa])
        # Find employees without SSA information
        employees_without_ssa =  ssa_set - employees_set

        employees_without_ssa = list(employees_without_ssa)

        current_year = datetime.now().year
        query_ssa2 = frappe.db.sql(
            """
            SELECT 
                '401N' as tax_type,
                c.tax_id,
                row_number() over(order by ssa.employee) as idx,
                replace(emp.custom_citizen_id, '-', '') as citizen_id,
                ssa.employee,
                ssa.company,
                emp.custom_prefix as prefix,
                emp.first_name,
                emp.last_name,
                emp.custom_directorate,
                ssa.taxable_earnings_till_date as pay_amount,
                ssa.tax_deducted_till_date as deduct_amount,
                '1' as tax_cond,
                emp.custom_house_no,
                emp.custom_village_building,
                emp.custom_soi,
                emp.custom_street,
                emp.custom_subdistrict,
                emp.custom_district,
                emp.custom_province,
                emp.custom_zip_code
            FROM 
                `tabSalary Structure Assignment` ssa

            left outer join `tabEmployee` emp on emp.name = ssa.employee
            left outer join `tabCompany` c on c.name = ssa.company

            WHERE 
                ssa.taxable_earnings_till_date IS NOT NULL
                AND ssa.tax_deducted_till_date IS NOT NULL
                AND ssa.employee IN %(employee_ids)s
                AND ssa.from_date = (
                    SELECT MAX(sub_ssa.from_date)
                    FROM `tabSalary Structure Assignment` sub_ssa
                    WHERE sub_ssa.employee = ssa.employee
                )
                AND YEAR(emp.relieving_date) = %(current_year)s

            """,
            {"employee_ids": tuple(employees_without_ssa), "current_year": current_year},
            as_dict=True,
        )
        data_ssa2 = query_ssa2

        for row_ssa in data_ssa2:
            row_ssa['idx'] = len(data_res) + 1
            data_res.append(row_ssa)

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