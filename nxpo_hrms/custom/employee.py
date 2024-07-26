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
    def custom_years_of_experience(self):
        transitions = frappe.get_all(
            "Employee Transition",
            fields=[
                "employee",
                "transition_date as from_date",
                "end_date as to_date",
            ],
            filters={
                "employee": self.employee,
                "docstatus": 1,
            },
            order_by="transition_date asc",
            limit_page_length=1
        )

        if transitions[0]['from_date']:
            from_date = transitions[0]['from_date']
            date = self.relieving_date or today()
            diff = relativedelta(getdate(date), getdate(from_date))
            custom_years_of_experience = _("{0} Years {1} Months {2} Days").format(
                diff.years, diff.months, diff.days
            )
            return custom_years_of_experience
        else:
            return ""



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

def update_employee_data(doc, method=None):
    # Date pass probation
    doc.custom_date_pass_probation = (
        getdate(doc.date_of_joining) +
        relativedelta(days=doc.custom_probation_days)
    )
    # Relieving Date from Effective Date
    doc.relieving_date = doc.custom_exit_effective_date and (
        getdate(doc.custom_exit_effective_date) -
        relativedelta(days=1)
    ) or ""

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

@frappe.whitelist()
def get_employee_basic_html(employee):
    data = json.loads(employee)
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
            "school_univ as school",
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




