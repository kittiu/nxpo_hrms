# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime



def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data

def add_space_character(amount=0):
    if amount: 
        space = " " * amount
    else: 
        space = ""
    return space

def chk_character(names=None, amount=0):
    if names is None:
        names = ""
    if len(names) < amount:
        # names = names.ljust(amount)
        # print("len", len(names))
        len_name = len(names)
        last_amount = amount - len_name
        space = " " * last_amount
        names = names + space
        

    return names

def add_zero_front(num=None, amount=0):
    return str(num).zfill(amount)

def format_total_net_pay(total_net_pay, total_length=19):
    # Convert total_net_pay to string if it's not already
    total_net_pay = str(total_net_pay)
    
    # Remove the decimal point and pad with zeros if necessary
    if '.' in total_net_pay:
        integer_part, decimal_part = total_net_pay.split('.')
        decimal_part = decimal_part.ljust(2, '0')  # Ensure 2 decimal places
    else:
        integer_part, decimal_part = total_net_pay, '00'

    # Combine integer and decimal parts, then pad with leading zeros
    combined = integer_part + decimal_part
    return combined.zfill(total_length)



def get_columns(filters):
    label = ""
    count_batch = frappe.db.count('Salary Slip', {
        'company': filters.get('company'), 
        'docstatus': filters.get('docstatus'),
        'posting_date': ['between', [filters.get('from_date'), filters.get('to_date')]]
    })

    # Calculate the total net pay
    total_net_pay = frappe.db.get_value('Salary Slip', 
        filters={
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            'posting_date': ['between', [filters.get('from_date'), filters.get('to_date')]]
        }, 
        fieldname='SUM(net_pay)'
    )

    posting_date = frappe.db.get_value( 'Salary Slip', 
        filters={
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            'posting_date': ['between', [filters.get('from_date'), filters.get('to_date')]]
        }, 
        fieldname='posting_date'
    )
    posting_date_transform = "00000000"
    if posting_date:
        posting_date_transform = posting_date.strftime('%d%m%Y')
    # Field Type > 1-2 (Fixed)
    result_1 = "10"

    # Record Type >  3 (Fixed)
    result_2 = "1"

    # Batch Number > 4-9 (Fixed)
    result_3 = "000001"

    # รหัสธนาคารผู้ส่งข้อมูล > 10-12
    result_4 = "006"

    # จำนวนรายการทั้งหมดใน Batch > 13-19
    result_5 = add_zero_front(count_batch, 7)

    # จำนวนเงินทั้งหมดใน Batch > 20-38
    result_6 = format_total_net_pay(total_net_pay, 19)

    # "วันที่รายการมีผล DDMMYYYY (YYYY = ปีค.ศ.)" > 39-46
    result_7 = posting_date_transform

    # D = Debit C = Credit > 47-47
    result_8 = "C"

    # Abbreviation of activities > 48-55
    result_9 = "00000000"

    # Company ID on KTB  > 56-71 
    result_10 = add_space_character(16)

    # Company ID on KTB  > 56-71 
    result_11 = add_space_character(16)

    # space  > 72-91 
    result_12 = add_space_character(20)

    # space > 92-498 
    result_13 = add_space_character(407)


    label = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_8 + result_9 + result_10 + result_11 + result_12 + result_13

    columns = [
        {
        "fieldname": "result_mix",
        "fieldtype": "Data",
        "label": label,
        "width": 1000
        }
    ]

    return columns

def get_data(filters):
    data = []

    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    # Parse the dates
    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
    to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

    # Check if the month and year are the same
    same_month = (from_date_obj.year == to_date_obj.year) and (from_date_obj.month == to_date_obj.month)

    if same_month != True:
        return data

    query = f"""
        SELECT 
            ss.employee, 
            ss.employee_name, 
            ss.net_pay,
            emp.custom_bank_branch_code as bank_branch_code,
            emp.bank_ac_no,
            ss.posting_date
        FROM `tabSalary Slip` ss
        join `tabEmployee` emp on ss.employee = emp.employee 
        WHERE ss.docstatus = %(docstatus)s
            AND ss.company = %(company)s 
            AND ss.posting_date >= %(from_date)s 
            AND ss.posting_date <= %(to_date)s 
        """
    
    query_data = frappe.db.sql(query, filters, as_dict=True)

    data = query_data

    branch_code, bank_account_no, account_name = frappe.db.get_value('Bank Account', 
        filters={
            'account_name': "Office of National Higher Education Science Research and Innovation Policy Council", 
            'company': filters.get('company'), 
        }, 
        fieldname='branch_code, bank_account_no, account_name'
    )

    
    for row in data:
        # กำหนดค่าเท่ากับ 10 > 1-2
        result_1 = "10"

        # กำหนดค่าเท่ากับ 2 > 3-3
        result_2 = "2"

        # Running No. > 4-9
        result_3 = "000001"

        # รหัสธนาคารของบัญชีปลายทาง > 10-12
        result_4 = "006"

        # ใส่รหัสสาขาปลายทาง > 13-16
        result_5 = add_zero_front(row['bank_branch_code'], 4) 

        # เลขที่บัญชีปลายทาง > 17-27
        result_6 = add_zero_front(row['bank_ac_no'], 11)

        # รหัสธนาคารต้นทาง > 28-30
        result_7 = "006"

        # รหัสสาขาธนาคารต้นทาง > 31-34
        result_8 = branch_code if branch_code else "0000"

        # เลขที่บัญชีเงินฝากธนาคารต้นทาง > 35-45
        result_9 = bank_account_no if add_zero_front(bank_account_no, 11) else "00000000000" 

        row_posting_date_transform = "00000000"
        if row['posting_date']:
            row_posting_date_transform = row['posting_date'].strftime('%d%m%Y')

        # วันที่รายการมีผล DDMMYYYY > 46-53
        result_10 = row_posting_date_transform

        # กำหนดค่าตามประเภทรายการ > 54-55
        result_11 = "02"

        # รหัส Clearing House > 56-57
        result_12 = "00"

        # จำนวนเงินโอน > 58-74
        result_13 = format_total_net_pay(row['net_pay'], 17)

        # Abbreviation of Activities > 75-82
        result_14 = add_space_character(8)

        # Receiver ID > 83-92
        result_15 = "0000000000"

        # ชือผู้รับโอน > 93-192
        name_result_16= row['employee_name']
        result_16 = chk_character(name_result_16, 100)

        # ชื่อผู้โอน > 193-292
        name_result_17 = account_name
        # name_result_17= "Office of National Higher Education Science Research and Innovation Policy Council"
        result_17 = chk_character(name_result_17, 100)
        
        # Other Info 1 > 293-332
        result_18 = add_space_character(40)

        # รหัสอ้างอิงการสมัคร DDA Ref 1 > 333-350
        result_19 = add_space_character(18)

        # space > 351-352
        result_20 = add_space_character(2)

        # space > 353-370
        result_21 = add_space_character(18)

        # space > 371-372
        result_22 = add_space_character(2)

        # space > 373-392
        result_23 = add_space_character(20)

        # เลขที่อ้างอิงกำหนดโดยธนาคาร > 393-398
        result_24 = "000001"

        # สถานะของรายการ
        result_25 = "09"

        # Combine the results into a single string
        results = [
            result_1, result_2, result_3, result_4, result_5, result_6,
            result_7, result_8, result_9, result_10, result_11, result_12,
            result_13, result_14, result_15, result_16, result_17, result_18,
            result_19, result_20, result_21, result_22, result_23, result_24, result_25
        ]

        row['result_mix'] = "".join(results)

    return data
