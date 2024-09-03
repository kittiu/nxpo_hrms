# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from dateutil.relativedelta import relativedelta
from frappe.utils import (
    getdate,
    today,
)
import json
from hrms.overrides.employee_master import EmployeeMaster
import re
from datetime import datetime


class EmployeeNXPO(EmployeeMaster):

    @property
    def custom_experience_ytd(self):
        # Experience YTD
        date = self.relieving_date or today()
        diff = relativedelta(getdate(date), getdate(self.date_of_joining))
        custom_experience_ytd = _("{0} Years {1} Months {2} Days").format(
            diff.years, diff.months, diff.days
        )
        return custom_experience_ytd


    @property
    def custom_years_of_current_designation(self):
        total_duration = get_custom_years_of_current_designation(self.employee)
        return total_duration

    @property
    def custom_business_unit(self):
        names = []
        if self.custom_subdepartment:
            names.append(frappe.get_value(
                "Department", self.custom_subdepartment, "department_name", cache=True
            ))
        if self.department:
            names.append(frappe.get_value(
                "Department", self.department, "department_name", cache=True
            ))
        if self.custom_directorate:
            names.append(frappe.get_value(
                "Department", self.custom_directorate, "department_name", cache=True
            ))
        return ", ".join(names)
    

def get_custom_years_of_current_designation(employee_code):
    transitions = frappe.get_all(
        "Employee Transition",
        fields=[
                "employee",
                "designation",
                "duration",
                "transition_date as from_date",
                "end_date as to_date",
            ],
            filters={
                "employee": employee_code,
                "docstatus": 1,
            },
            order_by="transition_date desc",
    )

    total_duration = relativedelta(years=0, months=0, days=0)
    last_personal_grade = None

    # for i in range(len(transitions)):
    for transition in transitions:
        # transition = transitions[i]
        personal_grade = frappe.db.get_value('Designation', transition.designation, 'custom_personal_grade')
            
        if last_personal_grade is None:
            last_personal_grade = personal_grade

        if personal_grade != last_personal_grade:
            break

        if transition.duration is None:
            from_date = transition.from_date
            to_date = datetime.now().date()  # Get current date
            transition_duration = get_duration(from_date, to_date)
            transition_duration = parse_duration(transition_duration)
        else:
            transition_duration = parse_duration(transition.duration)

        # duration = parse_duration(transition.duration)
        total_duration += transition_duration 

    total_duration = normalize_relativedelta(total_duration)
    total_duration = format_duration(total_duration)
    return total_duration

def parse_duration(duration_str):
    # Assuming duration_str is in the format 'X Years Y Months Z Days'
    years, months, days = 0, 0, 0
    if 'Years' in duration_str:
        years = int(duration_str.split(' Years ')[0])
        duration_str = duration_str.split(' Years ')[1]
    if 'Months' in duration_str:
        months = int(duration_str.split(' Months ')[0])
        duration_str = duration_str.split(' Months ')[1]
    if 'Days' in duration_str:
        days = int(duration_str.split(' Days')[0])
    return relativedelta(years=years, months=months, days=days)

def format_duration(rd):
    return f"{rd.years} Years {rd.months} Months {rd.days} Days"

def normalize_relativedelta(rd):
    temp_start_date = datetime(1, 1, 1)
    normalized_date = temp_start_date + rd
    normalized_rd = relativedelta(normalized_date, temp_start_date)
    return normalized_rd

# Helper function to calculate duration between two dates
def get_duration(from_date, to_date):
    delta = relativedelta(to_date, from_date)
    return f"{delta.years} Years {delta.months} Months {delta.days} Days"

def update_employee_data(doc, method=None):
    # Date pass probation
    doc.custom_date_pass_probation = (
        getdate(doc.date_of_joining) +
        relativedelta(days=doc.custom_probation_days) -
        relativedelta(days=1)
    )
    # Relieving Date from Effective Date
    doc.relieving_date = doc.custom_exit_effective_date and (
        getdate(doc.custom_exit_effective_date) -
        relativedelta(days=1)
    ) or ""
    # PIN
    doc.custom_pin = get_last_valid_integer(doc.name)

def get_last_valid_integer(input_string):
    parts = re.split(r'\D+', input_string)
    integers = [int(part) for part in parts if part.isdigit()]
    return str(integers[-1]) if integers else ""

def update_current_address(doc, method=None):
    addrs = [
        doc.custom_house_no,
        doc.custom_soi,
        doc.custom_street,
        doc.custom_subdistrict,
        doc.custom_district,
        doc.custom_province,
        doc.custom_zip_code
    ]
    addrs = [x for x in addrs if x != None]
    doc.current_address = ", ".join(addrs)

def update_permanent_address(doc, method=None):
    addrs = [
        doc.custom_perm_house_no,
        doc.custom_perm_soi,
        doc.custom_perm_street,
        doc.custom_perm_subdistrict,
        doc.custom_perm_district,
        doc.custom_perm_province,
        doc.custom_perm_zip_code
    ]
    addrs = [x for x in addrs if x != None]
    doc.permanent_address = ", ".join(addrs)

@frappe.whitelist()
def get_employee_basic_html(employee):
    
    data = json.loads(employee)

    # Convert date_of_birth to a date object
    date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()

    # Calculate age
    today = datetime.today().date()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    data['age'] = f"{age} ปี"

    return frappe.render_template("nxpo_hrms/custom/employee/basic.html", {"data": data})

@frappe.whitelist()
def get_employee_transition_html(employee):
    trans = frappe.get_all(
        "Employee Transition",
        fields=[
            "employee",
            "department",
            "directorate",
            "designation",
            "transition_date as from_date",
            "end_date as to_date",
            "duration",
            "organization"
        ],
        filters={
            "docstatus": 1,
            "employee": employee,
        },
        order_by="employee, transition_date desc",
    )
    for rec in trans:
        rec["directorate"] = frappe.get_value(
            "Department",
            rec["directorate"],
            "department_name",  # To remove - N suffix
            cache=True
        )
        rec["department"] = frappe.get_value(
            "Department",
            rec["department"],
            "department_name",  # To remove - N suffix
            cache=True
        )
        if rec['duration'] is None:
            date = today()
            diff = relativedelta(getdate(date), getdate(rec['from_date']))
            custom_duration = _("{0} Years {1} Months {2} Days").format(
                diff.years, diff.months, diff.days
            )
            rec['duration'] = custom_duration
  


    return frappe.render_template("nxpo_hrms/custom/employee/employee_transition.html", {"data": trans})

@frappe.whitelist()
def get_external_work_html(employee):
    externals = frappe.get_all(
        "Employee External Work History",
        fields=[
            "parent as employee",
            "company_name as company",
            "designation",
            "custom_date_joining as from_date",
            "custom_relieving_date as to_date",
        ],
        filters={
            "parent": employee
        },
        order_by="parent, custom_date_joining desc",
    )
    return frappe.render_template("nxpo_hrms/custom/employee/external_work.html", {"data": externals})


@frappe.whitelist()
def get_education_html(employee):
    educations = frappe.get_all(
        "Employee Education",
        fields=[
            "custom_schooluniversity as school",
            "custom_degree as degree",
            "custom_major as major",
            "custom_year_of_admission as admission_year",
            "maj_opt_subj",
        ],
        filters={
            "parent": employee
        },
        order_by="parent, custom_year_of_admission desc",
    )
    return frappe.render_template("nxpo_hrms/custom/employee/education.html", {"data": educations})

@frappe.whitelist()
def get_employee_special_assignment(employee):
    employee_special_assignment = frappe.get_all(
        "Employee Special Assignment",
        fields=[
            "assignment_type as type",
            "designation",
            "department",
            "directorate",
            "from_date",
            "to_date",
            "duration"
        ],
        filters={
            "employee": employee
        },
        order_by="from_date desc",
    )

    for esa in employee_special_assignment:
        esa["directorate"] = frappe.get_value(
            "Department",
            esa["directorate"],
            "department_name",  # To remove - N suffix
            cache=True
        )
        esa["department"] = frappe.get_value(
            "Department",
            esa["department"],
            "department_name",  # To remove - N suffix
            cache=True
        )

    return frappe.render_template("nxpo_hrms/custom/employee/employee_special_assignment.html", {"data": employee_special_assignment})




