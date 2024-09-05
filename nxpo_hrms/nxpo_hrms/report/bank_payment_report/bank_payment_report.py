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
    if num is None:
        return None
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

def get_sum_bonus(filters, type_bonus=None):
    date_field = 'custom_date_for_split_tax_component' if filters.get('nob') == 'bonus' else 'posting_date'

    ssl_bonus = frappe.get_all('Salary Slip', 
        filters={
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            date_field: filters.get('date'),
            'custom_split_tax_deduction_on': ['is', 'set'],
        }, 
        fields=[
            'name',
            'custom_split_tax_deduction_on', 
            'custom_main_tax_deduct_amount as main_tax_deduct_amount',
            'custom_split_tax_deduct_amount as split_tax_deduct_amount'
        ]
    )

    bonus_paid = 0
    excluded_bonus = 0
    for row in ssl_bonus:
        # if type_bonus is 'bonus_paid' and row['custom_split_tax_deduction_on']:
        sum_net_bonus_paid = frappe.db.get_value('Salary Detail', 
            filters={
                'parent': row['name'], 
                'parentfield': 'earnings',
                'salary_component': row['custom_split_tax_deduction_on']
            }, 
            fieldname='SUM(amount)'
            )
        split_tax_deduct_amount = round(row.get('split_tax_deduct_amount', 0), 2)
        sum_net_bonus_paid = (sum_net_bonus_paid or 0) - split_tax_deduct_amount
        bonus_paid = bonus_paid + (sum_net_bonus_paid or 0)
        bonus_paid = round(bonus_paid, 2)


        sum_net_excluded_bonus = frappe.db.get_value('Salary Detail', 
            filters={
                'parent': row['name'], 
                'parentfield': 'earnings',
                'salary_component': ['!=', row['custom_split_tax_deduction_on']]
            }, 
            fieldname='SUM(amount)'
        )
        main_tax_deduct_amount = round(row.get('main_tax_deduct_amount', 0), 2)
        sum_net_excluded_bonus = (sum_net_excluded_bonus or 0) - main_tax_deduct_amount
        excluded_bonus = excluded_bonus + (sum_net_excluded_bonus or 0) 
        excluded_bonus = round(excluded_bonus, 2)
        
    
    if type_bonus is 'bonus_paid':
        return bonus_paid
    elif type_bonus is 'excluded_bonus': 
        return excluded_bonus


def get_columns(filters):
    label = ""
    count_batch = 0

    if filters.get('nob') == 'bonus':
        count_batch = frappe.db.count('Salary Slip', {
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            'custom_date_for_split_tax_component': filters.get('date'),
            'custom_split_tax_deduction_on': ['is', 'set']
        })
    else:
        count_batch = frappe.db.count('Salary Slip', {
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            'posting_date': filters.get('date'),
        })
        
    # Calculate the total net pay
    sum_net_pay = frappe.db.get_value('Salary Slip', 
        filters={
            'company': filters.get('company'), 
            'docstatus': filters.get('docstatus'),
            'posting_date': filters.get('date'),
            'custom_split_tax_deduction_on': ['is', 'null']
        }, 
        fieldname='SUM(net_pay)'
    )
    # print('sum_net_pay', sum_net_pay)

    sum_bonus_paid = get_sum_bonus(filters, 'bonus_paid')
    # print('sum_bonus_paid', sum_bonus_paid)
    sum_excluded_bonus = get_sum_bonus(filters, 'excluded_bonus')
    # print('sum_excluded_bonus', sum_excluded_bonus)

    total_net_pay = 0
    if filters.get('nob') == 'normal':
        total_net_pay = (sum_net_pay or 0) + (sum_excluded_bonus or 0)
    else: 
        total_net_pay = (sum_bonus_paid or 0)

    # posting_date = frappe.db.get_value( 'Salary Slip', 
    #     filters={
    #         'company': filters.get('company'), 
    #         'docstatus': filters.get('docstatus'),
    #         'posting_date': filters.get('date'),
    #         # 'posting_date': ['between', [filters.get('from_date'), filters.get('to_date')]]
    #     }, 
    #     fieldname='posting_date'
    # )
    posting_date_transform =  "00000000"
    if filters.get('date'):
        # Convert the string to a datetime object
        date_str = filters.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Adjust the format based on your date string format

        # Now apply strftime to the datetime object
        posting_date_transform = date_obj.strftime('%d%m%Y')

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

    # space  > 72-91 
    result_11 = add_space_character(20)

    # space > 92-498 
    result_12 = add_space_character(407)


    label = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_8 + result_9 + result_10 + result_11 + result_12

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
    data_res = []
    # from_date = filters.get('from_date')
    # to_date = filters.get('to_date')
    # # Parse the dates
    # from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
    # to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

    # # Check if the month and year are the same
    # same_month = (from_date_obj.year == to_date_obj.year) and (from_date_obj.month == to_date_obj.month)

    # if same_month != True:
    #     return data
    conditions = get_conditions(filters)

    query = f"""
        SELECT 
            ss.name as id,
            ss.employee, 
            ss.employee_name, 
            ss.net_pay,
            emp.custom_bank_branch_code as bank_branch_code,
            emp.bank_ac_no,
            ss.posting_date,
            ss.custom_split_tax_deduction_on,
            ss.custom_main_tax_deduct_amount as main_tax_deduct_amount,
            ss.custom_split_tax_deduct_amount as split_tax_deduct_amount,
            ss.payroll_entry,
            emp.first_name,
            emp.last_name
        FROM `tabSalary Slip` ss
        join `tabEmployee` emp on ss.employee = emp.employee 
        WHERE ss.docstatus = %(docstatus)s
            AND ss.company = %(company)s 
            {('AND ' + conditions) if conditions else ''}
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
        # result_5 = add_zero_front(row['bank_branch_code'], 4) 
        if row['bank_branch_code'] is not None:
            result_5 = add_zero_front(row['bank_branch_code'], 4)
        else:
            result_5 = "0000"

        # เลขที่บัญชีปลายทาง > 17-27
        # result_6 = add_zero_front(row['bank_ac_no'], 11)

        # Handle the case where 'bank_ac_no' might be None
        if row['bank_ac_no'] is not None:
            result_6 = add_zero_front(row['bank_ac_no'], 11)
        else:
            result_6 = "00000000000"

        # รหัสธนาคารต้นทาง > 28-30
        result_7 = "006"

        # รหัสสาขาธนาคารต้นทาง > 31-34
        result_8 = branch_code if branch_code else "0000"

        # เลขที่บัญชีเงินฝากธนาคารต้นทาง > 35-45
        result_9 = bank_account_no if add_zero_front(bank_account_no, 11) else "00000000000" 

        row_posting_date_transform = "00000000"
        if row['custom_split_tax_deduction_on'] and row['payroll_entry'] and filters.get('nob') == 'bonus':
            payroll_entry_id = row['payroll_entry']
            date_split_tax_deduction_on = frappe.db.get_value('Payroll Entry', 
                filters={
                    'name': payroll_entry_id, 
                }, 
                fieldname='custom_date_for_split_tax_component'
            )
            if date_split_tax_deduction_on is not None:
                row_posting_date_transform = date_split_tax_deduction_on.strftime('%d%m%Y')
            else:
                row_posting_date_transform = ''         
        else:
            row_posting_date_transform = row['posting_date'].strftime('%d%m%Y')

        # วันที่รายการมีผล DDMMYYYY > 46-53
        result_10 = row_posting_date_transform

        # กำหนดค่าตามประเภทรายการ > 54-55
        result_11 = "02"

        # รหัส Clearing House > 56-57
        result_12 = "00"

        result_13 = "00000000000000000"
        # จำนวนเงินโอน > 58-74
        if row['custom_split_tax_deduction_on']:
            # Bonus Case
            if filters.get('nob') == 'bonus':
                total_split_tax = frappe.db.get_value('Salary Detail', 
                    filters={
                        'parent': row['id'], 
                        'parentfield': 'earnings', 
                        'salary_component': row['custom_split_tax_deduction_on']
                    }, 
                    fieldname='SUM(amount)'
                )
                split_tax_deduct_amount = round(row.get('split_tax_deduct_amount', 0), 2)
                total_split_tax = (total_split_tax or 0) - split_tax_deduct_amount
                result_13 = format_total_net_pay(total_split_tax, 17)
            # Excluded Case
            else: 
                total_split_tax = frappe.db.get_value('Salary Detail', 
                    filters={
                        'parent': row['id'], 
                        'parentfield': 'earnings', 
                        'salary_component': ['!=', row['custom_split_tax_deduction_on']]
                    }, 
                    fieldname='SUM(amount)'
                )
                main_tax_deduct_amount = round(row.get('main_tax_deduct_amount', 0), 2)
                total_split_tax = (total_split_tax or 0) - main_tax_deduct_amount
                
                result_13 = format_total_net_pay(total_split_tax, 17)

        else:
            result_13 = format_total_net_pay(row['net_pay'], 17)

        # Abbreviation of Activities > 75-82
        result_14 = add_space_character(8)

        # Receiver ID > 83-92
        result_15 = "0000000000"

        # ชือผู้รับโอน > 93-192
        # name_result_16 = row['employee_name']
        name_result_16 = row['first_name'] + '  ' + row['last_name']
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

        # สถานะของรายการ > 399-400
        result_25 = "09"

        # space > 401-498
        result_26 = add_space_character(98)

        # Combine the results into a single string
        results = [
            result_1, result_2, result_3, result_4, result_5, result_6,
            result_7, result_8, result_9, result_10, result_11, result_12,
            result_13, result_14, result_15, result_16, result_17, result_18,
            result_19, result_20, result_21, result_22, result_23, result_24, result_25, result_26
        ]

        result_mix = "".join(results)
        result_mix_json = {
                'result_mix': result_mix  # 'result_mix' as a string key
        }
        # row['result_mix'] = "".join(results)
        data_res.append(result_mix_json)

    # add row for split tax deduction => Excluded Bonus
    # print('data', data)
    # for row in data:
    #     if 'custom_split_tax_deduction_on' in row and row['custom_split_tax_deduction_on']:
    #         result_1 = "10" 
    #         result_2 = "2"
    #         result_3 = "000001"
    #         result_4 = "006"
    #         if row['bank_branch_code'] is not None:
    #             result_5 = add_zero_front(row['bank_branch_code'], 4)
    #         else:
    #             result_5 = "0000"
            
    #         if row['bank_ac_no'] is not None:
    #             result_6 = add_zero_front(row['bank_ac_no'], 11)
    #         else:
    #             result_6 = "00000000000"
    #         result_7 = "006"
    #         result_8 = branch_code if branch_code else "0000"
    #         result_9 = bank_account_no if add_zero_front(bank_account_no, 11) else "00000000000" 
    #         row_posting_date_transform = "00000000"
    #         if row['posting_date']:
    #             row_posting_date_transform = row['posting_date'].strftime('%d%m%Y')
    #         result_10 = row_posting_date_transform
    #         result_11 = "02"
    #         result_12 = "00"
    #         if row['custom_split_tax_deduction_on'] is not None:
    #             print('custom_split_tax_deduction_on', row['custom_split_tax_deduction_on'])
    #             total_split_tax = frappe.db.get_value('Salary Detail', 
    #                 filters={
    #                     'parent': row['id'], 
    #                     'parentfield': 'earnings', 
    #                     'salary_component': ['!=', row['custom_split_tax_deduction_on']]
    #                 }, 
    #                 fieldname='SUM(amount)'
    #             )
    #             total_split_tax = (total_split_tax or 0) - row['main_tax_deduct_amount']
    #             # row Bonus Paid 
    #             result_13 = format_total_net_pay(total_split_tax, 17)

    #         else:
    #             result_13 = format_total_net_pay(row['net_pay'], 17)
    #         result_14 = add_space_character(8)
    #         result_15 = "0000000000"
    #         name_result_16= row['employee_name']
    #         result_16 = chk_character(name_result_16, 100)
    #         name_result_17 = account_name
    #         result_17 = chk_character(name_result_17, 100)
    #         result_18 = add_space_character(40)
    #         result_19 = add_space_character(18)
    #         result_20 = add_space_character(2)
    #         result_21 = add_space_character(18)
    #         result_22 = add_space_character(2)
    #         result_23 = add_space_character(20)
    #         result_24 = "000001"
    #         result_25 = "09"
    #         results = [
    #             result_1, result_2, result_3, result_4, result_5, result_6,
    #             result_7, result_8, result_9, result_10, result_11, result_12,
    #             result_13, result_14, result_15, result_16, result_17, result_18,
    #             result_19, result_20, result_21, result_22, result_23, result_24, result_25
    #         ]

    #         test = "".join(results)
    #         test1 = {
    #             'result_mix': test  # 'result_mix' as a string key
    #         }
    #         data_res.append(test1)
            

    # print('data_res', data_res)
    return data_res


    
def get_conditions(filters):
    conditions = []

    if filters.get("nob") == 'normal':
        conditions.append("ss.posting_date = %(date)s")

    if filters.get("nob") == 'bonus':
        conditions.append("ss.custom_date_for_split_tax_component = %(date)s")


    # Combine conditions into a single string
    return " AND ".join(conditions)
