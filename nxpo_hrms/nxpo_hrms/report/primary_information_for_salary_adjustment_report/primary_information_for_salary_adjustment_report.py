# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime



def execute(filters=None):
    columns = get_columns(filters)
    data = get_data_entry(filters)

    return columns, data



def get_columns(filters):
    columns = [
        {
            "fieldname": "employee",
            "fieldtype": "Data",
            "label": 'รหัสพนักงาน',
            "width": 0
        },
        {
            "fieldname": "prefix",
            "fieldtype": "Data",
            "label": "คำนำหน้าชื่อ",
            "width": 0
        },
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": 'ชื่อ-สกุล',
            "width": 0
        },
        {
            "fieldname": "designation",
            "fieldtype": "Data",
            "label": 'ตำแหน่ง',
            "width": 0
        },
        {
            "fieldname": "directorate",
            "fieldtype": "Data",
            "label": 'ชื่อกลุ่ม/ฝ่าย',
            "width": 0
        },
        {
            "fieldname": "employment_type",
            "fieldtype": "Data",
            "label": 'ประเภท',
            "width": 0
        },
        {
            "fieldname": "grade",
            "fieldtype": "Data",
            "label": 'ระดับ',
            "width": 0
        },
        {
            "fieldname": "date_of_joining",
            "fieldtype": "Date",
            "label": 'วันเริ่มงาน',
            "width": 0
        },
        {
            "fieldname": "date_pass_probation",
            "fieldtype": "Date",
            "label": 'วันครบทดลองงาน',
            "width": 0
        },
        {
            "fieldname": "test_work",
            "fieldtype": "Data",
            "label": 'ทดลองงาน',
            "width": 0
        },
        {
            "fieldname": "exit_effective_date",
            "fieldtype": "Date",
            "label": 'สถานะลาออก',
            "width": 0
        },
        {
            "fieldname": "period_work_before",
            "fieldtype": "Data",
            "label": 'ระยะเวลาปฏิบัติงานสัดส่วน (ก่อนหัก)',
            "width": 0
        },
        {
            "fieldname": "deduct_other",
            "fieldtype": "Data",
            "label": 'หักกรณีต่างๆ (เดือน)',
            "width": 0
        },
        {
            "fieldname": "deduct_result",
            "fieldtype": "Data",
            "label": 'ระยะเวลาปฏิบัติงานสัดส่วน',
            "width": 0
        },
        {
            "fieldname": "remark",
            "fieldtype": "Data",
            "label": 'หมายเหตุ',
            "width": 0
        },
        {
            "fieldname": "base_salary",
            "fieldtype": "Currency",
            "label": 'อัตราเงินเดือน',
            "width": 0
        },
        {
            "fieldname": "custom_salary_amount",
            "fieldtype": "Currency",
            "label": 'เงินเดือนเดือนล่าสุดที่ได้รับ',
            "width": 0
        }
    ]

    return columns
    
def calculate_months(date_of_joining, custom_date_pass_probation):
    # Ensure the dates are in datetime.date format
    if isinstance(date_of_joining, str):
        date_of_joining = datetime.strptime(date_of_joining, "%Y-%m-%d").date()
    if isinstance(custom_date_pass_probation, str):
        custom_date_pass_probation = datetime.strptime(custom_date_pass_probation, "%Y-%m-%d").date()

    months_diff = (custom_date_pass_probation.year - date_of_joining.year) * 12 + custom_date_pass_probation.month - date_of_joining.month

    days_diff = (custom_date_pass_probation - date_of_joining).days - (months_diff * 30)

    if days_diff >= 15:
        months_diff += 1

    if months_diff >= 12:
        return 12
    else:
        return months_diff

def get_data(filters):
    data = []
    query_data = frappe.db.sql(
        """SELECT
            emp.name AS employee,
            emp.employee_name,
            emp.designation,
            emp.custom_directorate AS directorate,
            emp.employment_type,
            emp.grade,
            emp.date_of_joining,
            emp.custom_date_pass_probation AS date_pass_probation,
            emp.custom_exit_effective_date AS exit_effective_date,
            emp.custom_borrow_start_date,
            emp.custom_borrow_end_date,
            emp.custom_prefix as prefix

        FROM `tabEmployee` emp 
        WHERE emp.custom_date_pass_probation <= %(year_end_date)s
            AND emp.company = %(company)s   
        """,
        filters,
        as_dict=True,
    )

    
    data = query_data


    for rows in data:
        rows['test_work'] = "พ้นทดลองงาน"
        period_work_before = calculate_months(rows['date_of_joining'], filters.get('year_end_date'))
        rows['period_work_before'] = period_work_before
        employee = rows['employee']

        base_salary, custom_salary_amount = get_latest_salary_structure(employee)
        # print('base_salary', base_salary)
        rows['base_salary'] = base_salary
        rows['custom_salary_amount'] = custom_salary_amount

        if rows['employment_type'] == 'พนักงานลาไปศึกษา':
            
            deduct_other = None

            borrow_start_date = rows['custom_borrow_start_date']
            borrow_end_date = rows['custom_borrow_end_date']

            if borrow_start_date is not None and borrow_start_date is not None:
                deduct_other = calculate_months(borrow_start_date, borrow_end_date)
                deduct_result = period_work_before - deduct_other
                rows['deduct_result'] = deduct_result
                if deduct_other == 12:
                    rows['remark'] = "ลาศึกษาต่อตลอดปีงบประมาณ"
                else:
                    rows['remark'] = "ลาศึกษาต่อระหว่างปีงบประมาณ"
            else:
                deduct_other = None
                rows['deduct_result'] = period_work_before
                rows['remark'] = ""


            rows['deduct_other'] = deduct_other
        
        elif rows['employment_type'] == 'พนักงานไปปฏิบัติงานที่หน่วยงานอื่น - ไม่จ่ายเงินเดือน':
            rows['remark'] = "พนักงานไปปฏิบัติงานที่หน่วยงานอื่น - ไม่จ่ายเงินเดือน"
            rows['deduct_other'] = ""
            rows['deduct_result'] = period_work_before

        else:
            rows['remark'] = ""
            rows['deduct_other'] = ""
            rows['deduct_result'] = period_work_before
    
    return data

def get_data_entry(filters):

    # data = get_conncet_hook(filters)
    fiscal_dict = frappe.db.get_value('Fiscal Year', filters.get('fiscal_year'), ['year_start_date', 'year_end_date'], as_dict=1)
    # print('fiscal_dict', fiscal_dict)

    filters.year_start_date = fiscal_dict.year_start_date
    filters.year_end_date = fiscal_dict.year_end_date

    data = get_data(filters)

    return data

def get_latest_salary_structure(employee):
    query = """
        SELECT base, custom_salary_amount
        FROM `tabSalary Structure Assignment`
        WHERE docstatus = 1 AND employee = %s
        ORDER BY from_date DESC
        LIMIT 1
    """
    result = frappe.db.sql(query, employee, as_dict=True)
    
    if result:
        return result[0]['base'], result[0]['custom_salary_amount']
    else:
        return None, None 
    

# def get_conncet_hook(filters):
#     hook = frappe.get_hooks("get_data_primary_information_for_salary_adjustment_report")
    
#     if hook:
#         data_func = hook[0]
#         data = frappe.get_attr(data_func)(filters)
        
#     else:
#         data = []


#     return data
