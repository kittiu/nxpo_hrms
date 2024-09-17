# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data


def get_columns(filters):
    columns = [
        # {
        # "fieldname": "employee",
        # "fieldtype": "Link",
        # "label": "รหัสพนักงาน",
        # "options": "Employee",
        # "width": 0
        # },
        {
        "fieldname": "employee",
        "fieldtype": "Data",
        "label": "รหัสพนักงาน",
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
        "label": "ชื่อ",
        "width": 0
        },
        {
        "fieldname": "employment_type",
        "fieldtype": "Data",
        "label": "ประเภทพนักงาน",
        "width": 0
        },
        {
        "fieldname": "department",
        "fieldtype": "Data",
        "label": "สังกัด",
        "width": 0
        },
        {
        "fieldname": "custom_job_family",
        "fieldtype": "Data",
        "label": "กลุ่มตำแหน่ง",
        "width": 0
        },
        {
        "fieldname": "grade",
        "fieldtype": "Data",
        "label": "ระดับตำแหน่ง",
        "width": 0
        },
        {
        "fieldname": "custom_directorate",
        "fieldtype": "Data",
        "label": "Directorate",
        "width": 0
        },
        {
        "fieldname": "designation",
        "fieldtype": "Data",
        "label": "ตำแหน่ง",
        "width": 0
        },
        {
        "fieldname": "base_salary",
        "fieldtype": "Currency",
        "label": "อัตราเงินเดือน",
        "width": 0
        },
        {
        "fieldname": "e1",
        "fieldtype": "Currency",
        "label": "เงินเดือน",
        "width": 0
        },
        {
        "fieldname": "e2",
        "fieldtype": "Currency",
        "label": "เงินชดเชย 1",
        "width": 0
        },
        {
        "fieldname": "e3",
        "fieldtype": "Currency",
        "label": "เงินชดเชย 2",
        "width": 0
        },
        {
        "fieldname": "e4",
        "fieldtype": "Currency",
        "label": "ประโยชน์ตอบแทนอื่น",
        "width": 0
        },
        {
        "fieldname": "e5",
        "fieldtype": "Currency",
        "label": "เงินเพิ่มพิเศษ",
        "width": 0
        },
        {
        "fieldname": "e6",
        "fieldtype": "Currency",
        "label": "ตกเบิก",
        "width": 0
        },
        {
        "fieldname": "e7",
        "fieldtype": "Currency",
        "label": "เงินได้อื่นก่อนภาษี",
        "width": 0
        },
        {
        "fieldname": "e8",
        "fieldtype": "Currency",
        "label": "ค่าตอบแทนเหมาจ่าย",
        "width": 0
        },
        {
        "fieldname": "d1",
        "fieldtype": "Currency",
        "label": "ภาษี",
        "width": 0
        },
        {
        "fieldname": "d2",
        "fieldtype": "Currency",
        "label": "กองทุนสำรองเลี้ยงชีพ",
        "width": 0
        },
        {
        "fieldname": "d3",
        "fieldtype": "Currency",
        "label": "สหกรณ์ออมทรัพย์ วท.",
        "width": 0
        },
        {
        "fieldname": "d4",
        "fieldtype": "Currency",
        "label": "ธนาคารอาคารสงเคราะห์",
        "width": 0
        },
        {
        "fieldname": "d5",
        "fieldtype": "Currency",
        "label": "กยศ.",
        "width": 0
        },
        {
        "fieldname": "d6",
        "fieldtype": "Currency",
        "label": "เงินหักอื่นๆ",
        "width": 0
        },
        {
        "fieldname": "net_pay",
        "fieldtype": "Currency",
        "label": "รายได้สุทธิ",
        "width": 0
        },
        {
        "fieldname": "pvd_com",
        "fieldtype": "Currency",
        "label": "กองทุนฯสำนักงานสมทบ",
        "width": 0
        },
        {
        "fieldname": "gross_pay",
        "fieldtype": "Currency",
        "label": "รวมรายได้",
        "width": 0
        },
        {
        "fieldname": "total_deduction",
        "fieldtype": "Currency",
        "label": "รวมรายหัก",
        "width": 0
        },
        {
        "fieldname": "custom_min",
        "fieldtype": "Currency",
        "label": "Min",
        "width": 0
        },
        {
        "fieldname": "custom_max",
        "fieldtype": "Currency",
        "label": "Max",
        "width": 0
        },

        {
            "fieldname": "custom_percentile",
            "fieldtype": "Data",
            "label": "Percentile",
            "width": 0
        },
        {
        "fieldname": "posting_date",
        "fieldtype": "Date",
        "label": "Posting Date",
        "width": 0
        },

    ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    query = f"""
        SELECT
            ss.name as salary_slip_id,
            ss.employee,
            emp.custom_prefix as prefix,
            emp.employee_name,
            emp.department,
            emp.custom_job_family,
            emp.grade,
            emp.custom_directorate,
            emp.designation,
            e1.amount AS e1,
            e2.amount AS e2,
            e3.amount AS e3,
            e4.amount AS e4,
            e5.amount AS e5,
            e6.amount AS e6,
            e7.amount AS e7,
            d1.amount AS d1,
            d2.amount AS d2,
            d3.amount AS d3,
            d4.amount AS d4,
            d5.amount AS d5,
            d6.amount AS d6,
            e8.amount AS e8,
            ss.net_pay,
            pvd_com.amount AS pvd_com,
            ss.gross_pay,
            ss.total_deduction,
            gd.custom_min,
            gd.custom_max,
            ss.posting_date,
            emp.employment_type
        FROM `tabSalary Slip` ss
        JOIN `tabEmployee` emp ON ss.employee = emp.name
        JOIN `tabEmployee Grade` gd ON gd.name = emp.grade
        LEFT OUTER JOIN `tabSalary Detail` e1 ON e1.parenttype = 'Salary Slip' AND e1.parent = ss.name AND e1.salary_component = 'เงินเดือน'
        LEFT OUTER JOIN `tabSalary Detail` e2 ON e2.parenttype = 'Salary Slip' AND e2.parent = ss.name AND e2.salary_component = 'เงินชดเชย 1'
        LEFT OUTER JOIN `tabSalary Detail` e3 ON e3.parenttype = 'Salary Slip' AND e3.parent = ss.name AND e3.salary_component = 'เงินชดเชย 2'
        LEFT OUTER JOIN `tabSalary Detail` e4 ON e4.parenttype = 'Salary Slip' AND e4.parent = ss.name AND e4.salary_component = 'ประโยชน์ตอบแทนอื่น'
        LEFT OUTER JOIN `tabSalary Detail` e5 ON e5.parenttype = 'Salary Slip' AND e5.parent = ss.name AND e5.salary_component = 'เงินเพิ่มพิเศษ'
        LEFT OUTER JOIN `tabSalary Detail` e6 ON e6.parenttype = 'Salary Slip' AND e6.parent = ss.name AND e6.salary_component = 'ตกเบิก'
        LEFT OUTER JOIN `tabSalary Detail` e7 ON e7.parenttype = 'Salary Slip' AND e7.parent = ss.name AND e7.salary_component = 'เงินได้อื่นก่อนภาษี'
        LEFT OUTER JOIN `tabSalary Detail` d1 ON d1.parenttype = 'Salary Slip' AND d1.parent = ss.name AND d1.salary_component = 'ภาษี'
        LEFT OUTER JOIN `tabSalary Detail` d2 ON d2.parenttype = 'Salary Slip' AND d2.parent = ss.name AND d2.salary_component = 'กองทุนสำรองเลี้ยงชีพ'
        LEFT OUTER JOIN `tabSalary Detail` d3 ON d3.parenttype = 'Salary Slip' AND d3.parent = ss.name AND d3.salary_component = 'สหกรณ์ออมทรัพย์ วท.'
        LEFT OUTER JOIN `tabSalary Detail` d4 ON d4.parenttype = 'Salary Slip' AND d4.parent = ss.name AND d4.salary_component = 'ธนาคารอาคารสงเคราะห์'
        LEFT OUTER JOIN `tabSalary Detail` d5 ON d5.parenttype = 'Salary Slip' AND d5.parent = ss.name AND d5.salary_component = 'กยศ.'
        LEFT OUTER JOIN `tabSalary Detail` d6 ON d6.parenttype = 'Salary Slip' AND d6.parent = ss.name AND d6.salary_component = 'เงินหักอื่นๆ'
        LEFT OUTER JOIN `tabSalary Detail` pvd_com ON pvd_com.parenttype = 'Salary Slip' AND pvd_com.parent = ss.name AND pvd_com.salary_component = 'กองทุนสำรองเลี้ยงชีพสำนักงานสมทบ'
        LEFT OUTER JOIN `tabSalary Detail` e8 ON e8.parenttype = 'Salary Slip' AND e8.parent = ss.name AND e8.salary_component = 'ค่าตอบแทนเหมาจ่าย'
        WHERE ss.docstatus = %(docstatus)s
            AND ss.start_date >= %(from_date)s
            AND ss.end_date <= %(to_date)s
            AND ss.company = %(company)s {conditions}
        """
    
    query_data = frappe.db.sql(query, filters, as_dict=True)

    data = query_data

    #  Initialize totals
    sum_base = 0
    sum_e1 = 0
    sum_e2 = 0
    sum_e3 = 0
    sum_e4 = 0
    sum_e5 = 0
    sum_e6 = 0
    sum_e7 = 0
    sum_e8 = 0
    sum_d1 = 0
    sum_d2 = 0
    sum_d3 = 0
    sum_d4 = 0
    sum_d5 = 0
    sum_d6 = 0
    
    sum_custom_min = 0
    sum_custom_max = 0
    
    sum_net_pay = 0
    sum_gross_pay = 0
    sum_deductions = 0
    sum_pvd_com = 0

    for row in data:

        employee = row['employee']
        start = filters.get('from_date')
        end = filters.get('to_date')
        base_salary = get_latest_salary_structure(employee, start, end)
        row['base_salary'] = base_salary

        custom_min = row.get('custom_min', 0)
        custom_max = row.get('custom_max', 0)
        custom_base = base_salary if base_salary is not None else 0
        # row['custom_percentile'] = 5

        if base_salary is not None:
            if custom_min != custom_max:
                result1 = custom_base - custom_min
                result2 = custom_max - custom_min
                result3 = result1 / result2
                result4 = result3 * 100
                result4 = round(result4, 4)
                row['custom_percentile'] = f"{result4}"
            else: 
                row['custom_percentile'] = 0
        else:
            row['custom_percentile'] = 0
        
        # Calculate total amounts
        sum_e1 += row['e1'] if row['e1'] is not None else 0
        sum_e2 += row['e2'] if row['e2'] is not None else 0
        sum_e3 += row['e3'] if row['e3'] is not None else 0
        sum_e4 += row['e4'] if row['e4'] is not None else 0
        sum_e6 += row['e6'] if row['e6'] is not None else 0
        sum_e5 += row['e5'] if row['e5'] is not None else 0
        sum_e7 += row['e7'] if row['e7'] is not None else 0
        sum_e8 += row['e8'] if row['e8'] is not None else 0
        sum_d1 += row['d1'] if row['d1'] is not None else 0
        sum_d2 += row['d2'] if row['d2'] is not None else 0
        sum_d4 += row['d4'] if row['d4'] is not None else 0
        sum_d3 += row['d3'] if row['d3'] is not None else 0
        sum_d5 += row['d5'] if row['d5'] is not None else 0
        sum_d6 += row['d6'] if row['d6'] is not None else 0

        sum_custom_min += row['custom_min'] if row['custom_min'] is not None else 0
        sum_custom_max += row['custom_max'] if row['custom_max'] is not None else 0


        sum_base += base_salary if base_salary is not None else 0

        sum_net_pay += row['net_pay'] if row['net_pay'] is not None else 0
        sum_gross_pay += row['gross_pay'] if row['gross_pay'] is not None else 0
        sum_deductions += row['total_deduction'] if row['total_deduction'] is not None else 0
        sum_pvd_com += row['pvd_com'] if row['pvd_com'] is not None else 0

    # Append the total row
    # total_row = {
    #     'employee': 'Total',
    #     'e1': sum_e1,
    #     'e2': sum_e2,
    #     'e3': sum_e3,
    #     'e4': sum_e4,
    #     'e6': sum_e6,
    #     'e5': sum_e5,
    #     'e7': sum_e7,
    #     'e8': sum_e8,
    #     'd1': sum_d1,
    #     'd2': sum_d2,
    #     'd4': sum_d4,
    #     'd3': sum_d3,
    #     'd5': sum_d5,
    #     'd6': sum_d6,

    #     'base_salary': sum_base,

    #     'custom_min': sum_custom_min,
    #     'custom_max': sum_custom_max,

    #     'net_pay': sum_net_pay,
    #     'gross_pay': sum_gross_pay,
    #     'total_deduction': sum_deductions,
    #     'pvd_com': sum_pvd_com,
        
    #     'custom_percentile': None


    # }
    # data.append(total_row)

    return data

def get_conditions(filters):
    conditions = ""

    if filters.get("status_emp"):
        conditions += f"and emp.status = %(status_emp)s"
    
    if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
        conditions += f"and emp.custom_directorate = %(directorate)s"

    if filters.get("employment_type"):
        conditions += f"and emp.employment_type = %(employment_type)s"

    if filters.get("posting_date"):
        conditions += f"and ss.posting_date = %(posting_date)s"

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

def get_latest_salary_structure(employee, start, end):
    query = """
        SELECT base, from_date
        FROM `tabSalary Structure Assignment`
        WHERE docstatus = 1 
            AND employee = %(employee)s
        ORDER BY from_date DESC
        LIMIT 1
    """
    result = frappe.db.sql(query, {'employee': employee, 'start': start, 'end': end}, as_dict=True)
    if result:
        return result[0]['base']
    else:
        return None