# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _
from frappe.utils import getdate, today
from dateutil.relativedelta import relativedelta
from datetime import datetime


def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "fieldname": "full_name",
            "label": _("Full Name"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "directorate",
            "label": _("Directorate"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "type",
            "label": _("type"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "designation",
            "label": _("Designation"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "grade",
            "label": _("Grade"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "from_date",
            "label": _("From Date"),
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "to_date",
            "label": _("To Date"),
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "duration",
            "label": _("Duration"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "grade_duration",
            "label": _("Grade Duration"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "total_experience",
            "label": _("Total Experience"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "organization",
            "label": _("Organization"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "transition",
            "label": _("Transition"),
            "fieldtype": "Link",
            "options": "Employee Transition",
        },
    ]

def get_duration(from_date, to_date):
    diff = relativedelta(getdate(to_date), getdate(from_date))
    duration = _("{0} Years {1} Months {2} Days").format(
        diff.years, diff.months, diff.days
    )
    return duration

def get_data(filters):
    trans = get_employee_transition(filters)
    get_grade(trans)
    externals = get_external_work_history(filters)	
    # Merge 2 datasets
    employees = list(set([x.employee for x in trans] + [x.employee for x in externals]))
    employees.sort()
    final_data = []
    for e in employees:
        final_data += list(filter(lambda x: x.employee == e, trans))
        final_data += list(filter(lambda x: x.employee == e, externals))
    # Final formatting
    add_employee_data(final_data)
    
    format_today_duration(final_data)

    get_calculate_total_experience(final_data)

    get_grade_duration(final_data)

    if filters.get("ease_viewing"):
        format_easy_viewing(final_data)

    return final_data

def get_employee_transition(filters):
    # Get Employee Transition
    trans = []
    if filters.get("internal"):
        trans_filters = {
            "docstatus": 1,
        }
        if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
            employees = frappe.get_all(
                "Employee",
                filters=[["custom_directorate", "in", filters.get("directorate")]],
                pluck="name"
            )
            trans_filters["employee"] = ["in", employees]

        if filters.get("pmu_or_nxpo"):
            pmu_or_nxpo = filters.get("pmu_or_nxpo")
            if pmu_or_nxpo == 'pmu':
                employees = frappe.get_all(
                    "Employee",
                    filters=[["custom_directorate", "in", ["บพข. - N", "บพค. - N", "บพท. - N"]]],
                    pluck="name"
                )
                trans_filters["employee"] = ["in", employees]


            elif pmu_or_nxpo == 'nxpo':
                employees = frappe.get_all(
                        "Employee",
                        filters=[["custom_directorate", "not in", ["บพข. - N", "บพค. - N", "บพท. - N"]]],
                        pluck="name"
                )
                trans_filters["employee"] = ["in", employees]



        trans = frappe.get_all(
            "Employee Transition",
            fields=[
                "employee",
                "transition_type as type",
                "designation",
                "transition_date as from_date",
                "end_date as to_date",
                "duration",
                "company as organization",
                "name as transition"
            ],
            filters=trans_filters,
            order_by="employee, transition_date desc",
        )
    return trans

def get_external_work_history(filters):
    # Get External Works
    externals = []
    if filters.get("external"):
        external_filters = {}
        if filters.get("directorate") and filters.get("pmu_or_nxpo") is None:
            employees = frappe.get_all(
                "Employee",
                filters=[["custom_directorate", "in", filters.get("directorate")]],
                pluck="name"
            )
            external_filters["parent"] = ["in", employees]


        if filters.get("pmu_or_nxpo"):
            pmu_or_nxpo = filters.get("pmu_or_nxpo")
            if pmu_or_nxpo == 'pmu':
                employees = frappe.get_all(
                    "Employee",
                    filters=[["custom_directorate", "in", ["บพข. - N", "บพค. - N", "บพท. - N"]]],
                    pluck="name"
                )
                external_filters["parent"] = ["in", employees]


            elif pmu_or_nxpo == 'nxpo':
                employees = frappe.get_all(
                        "Employee",
                        filters=[["custom_directorate", "not in", ["บพข. - N", "บพค. - N", "บพท. - N"]]],
                        pluck="name"
                )
                external_filters["parent"] = ["in", employees]

            
        externals = frappe.get_all(
            "Employee External Work History",
            fields=[
                "parent as employee",
                "'ภายนอก' as type",
                "designation",
                "custom_date_joining as from_date",
                "custom_relieving_date as to_date",
                "company_name as organization",
            ],
            filters=external_filters,
            order_by="parent, custom_date_joining desc",
        )
    return externals

def add_employee_data(data):
    for rec in data:
        emp = frappe.get_cached_doc("Employee", rec.employee)
        rec["full_name"] = emp.employee_name
        rec["directorate"] = frappe.get_value(
            "Department",
            emp.custom_directorate,
            "department_name",  # use department_name to avoid -N suffix
            cache=True
        )

def format_easy_viewing(data):
    # If employee is same as previous, set blank for employee and full_name
    prev_employee = None
    for rec in data:
        skip = False
        if rec.get("employee") == prev_employee:
            skip = True
        prev_employee = rec.get("employee")
        if skip:
            rec["employee"] = ""
            rec["full_name"] = ""
            rec["directorate"] = ""

def format_today_duration(data):
    # For new transition without to_date, set as today
    for rec in data:
        if not rec.get("to_date"):
            rec["to_date"] = getdate(today())
        rec["duration"] = get_duration(rec.get("from_date"), rec.get("to_date"))


def get_calculate_total_experience(final_data):
    # cal total_experience by employee
    cal_total_exp = calculate_total_experience(final_data)

    # Initialize a set to keep track of processed employees
    processed_employees = set()

    for row in final_data:
        employee = row.get("employee") # Get the employee ID/name
        if employee:
            # If the employee is already processed, clear 'total_experience'
            if employee in processed_employees:
                row["total_experience"] = ""  # Clear for subsequent occurrences
            else:
                # Create a dictionary for faster lookup
                cal_total_exp_dict = {entry['employee']: entry['total_experience_value'] for entry in cal_total_exp}
                row["total_experience"] = cal_total_exp_dict.get(employee, None) 
                processed_employees.add(employee)  # Add employee to the processed set


def calculate_total_experience(data):
    total_exp = {}
    current_employee = None
    # Store the last entry for each employee to later update
    last_entries = {}
    
    for rec in data:
        if rec['full_name']:  # If current record has a full name, use it as the key
            current_employee = rec['employee']
            if current_employee not in total_exp:
                # Initialize storage for this employee
                total_exp[current_employee] = {'years': 0, 'from_date': None, 'to_date': None}

        # Assuming the dates are already datetime.date objects or None if missing
        from_date = rec['from_date'] if rec['from_date'] else datetime.today()
        to_date = rec['to_date'] if rec['to_date'] else datetime.today()

        duration = relativedelta(to_date, from_date)
        total_years = duration.years + duration.months / 12 + duration.days / 365.25
        
        # Accumulate the total experience for the current employee
        if current_employee:
            total_exp[current_employee]['years'] += total_years

            last_entries[current_employee] = rec  # Track the last entry for updating
    data = []
    # Format and update the final total experience and dates on the last record for each employee
    for emp, rec in last_entries.items():
        years, fractional_years = divmod(total_exp[emp]['years'], 1)
        months, fractional_months = divmod(fractional_years * 12, 1)
        days = int(fractional_months * 30)  # Approximation
        days += 1
        # rec['total_experience_value'] = f"{int(years)} Years {int(months)} Months {int(days)} Days"
        total_experience_value = f"{int(years)} Years {int(months)} Months {int(days)} Days"

        # Append a dictionary with the employee's data
        data.append({
            'employee': emp,
            'total_experience_value': total_experience_value,
        })


    return data
    

def get_grade(trans):
    # Fetch the grade data once
    grades = frappe.get_all(
        "Designation",
        fields=[
            "designation_name",
            "name",
            "custom_personal_grade as grade"
        ],
        order_by="name",
    )
    
    # Create a dictionary for faster lookup
    grade_dict = {entry['name']: entry['grade'] for entry in grades}

    for row in trans:
        designation = row['designation']
        # Assign the grade based on the designation
        row['grade'] = grade_dict.get(designation, None) 

def get_grade_duration(final_data):

    grade_obj = []
    grade_list = set()  # To track unique (employee, grade) combinations
    index = 0
    for row in final_data:
        employee = row.get("employee")
        grade = row.get("grade")

        if grade and (employee, grade) not in grade_list:
            index = index + 1
            grade_duration = relativedelta()
            # Append the combination only if it hasn't been seen
            emp_trans_by_emp_grade = [record for record in final_data if record['employee'] == employee and 'grade' in record and record['grade'] == grade]
            for trans_emp_grade in emp_trans_by_emp_grade:
                from_date = trans_emp_grade['from_date'] if trans_emp_grade['from_date'] else datetime.today()
                to_date = trans_emp_grade['to_date'] if trans_emp_grade['to_date'] else datetime.today()
                duration = relativedelta(to_date, from_date)
                grade_duration += duration
            
            # Calculate total days and convert to years, months, and days
            total_days = grade_duration.years * 365 + grade_duration.months * 30 + grade_duration.days

            # Calculate years, months, and remaining days
            years = total_days // 365
            remaining_days = total_days % 365

            months = remaining_days // 30
            days = remaining_days % 30
            grade_duration_value = "{0} Years {1} Months {2} Days".format(years, months, days)

            grade_obj.append({
                'employee': employee,
                'grade': grade,
                'grade_duration': grade_duration_value
            })
            grade_list.add((employee, grade))

    grade_lookup = { (entry['employee'], entry['grade']): entry['grade_duration'] for entry in grade_obj }
    grade_used = set()  # To track unique (employee, grade) combinations
    for row in final_data:
        employee = row.get("employee")
        grade = row.get("grade")
        
        # Check if either employee or grade is missing
        if not employee or not grade:
            continue  # Skip to the next iteration if either is missing

        # Check if the (employee, grade) combination has been seen
        if (employee, grade) in grade_used:
            row['grade_duration'] = ""
        else:
            if (employee, grade) in grade_lookup:
                row['grade_duration'] = grade_lookup[(employee, grade)]
            grade_used.add((employee, grade))  # Add the combination to the set




    
        


    