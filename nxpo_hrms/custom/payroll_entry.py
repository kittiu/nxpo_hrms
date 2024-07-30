# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from hrms.payroll.doctype.payroll_entry.payroll_entry import (
    set_fields_to_select,
	set_searchfield,
	set_filter_conditions,
	set_match_conditions
)
import ast


# Monkey patch function
def get_filtered_employees(
	sal_struct,
	filters,
	searchfield=None,
	search_string=None,
	fields=None,
	as_dict=False,
	limit=None,
	offset=None,
	ignore_match_conditions=False,
) -> list:
	SalaryStructureAssignment = frappe.qb.DocType("Salary Structure Assignment")
	Employee = frappe.qb.DocType("Employee")
	query = (
		frappe.qb.from_(Employee)
		.join(SalaryStructureAssignment)
		.on(Employee.name == SalaryStructureAssignment.employee)
		.where(
			(SalaryStructureAssignment.docstatus == 1)
			& (Employee.status != "Inactive")
			& (Employee.custom_no_salary != 1)  # kittiu
			& (Employee.company == filters.company)
			& ((Employee.date_of_joining <= filters.end_date) | (Employee.date_of_joining.isnull()))
			& ((Employee.relieving_date >= filters.start_date) | (Employee.relieving_date.isnull()))
			& (SalaryStructureAssignment.salary_structure.isin(sal_struct))
			& (SalaryStructureAssignment.payroll_payable_account == filters.payroll_payable_account)
			& (filters.end_date >= SalaryStructureAssignment.from_date)
		).orderby(Employee.name)
	)

	query = set_fields_to_select(query, fields)
	query = set_searchfield(query, searchfield, search_string, qb_object=Employee)
	query = set_filter_conditions(query, filters, qb_object=Employee)

	if not ignore_match_conditions:
		query = set_match_conditions(query=query, qb_object=Employee)

	if limit:
		query = query.limit(limit)

	if offset:
		query = query.offset(offset)

	return query.run(as_dict=as_dict)


# Hook method
def validate_posting_date(doc, method=None):
	if not (doc.start_date <= doc.posting_date <= doc.end_date):
		frappe.throw(_("Posting date must be between start date and end date"))


# API to get payroll entry summary
def sum_amount_ss_component(company, start_date, end_date, salary_component):
	ss = frappe.qb.DocType("Salary Slip")
	sd = frappe.qb.DocType("Salary Detail")
	total_amt = (
		frappe.qb.from_(ss)
		.inner_join(sd)
		.on(ss.name == sd.parent)
		.select(Sum(sd.amount))
		.where(
			(ss.docstatus == 1)
			& (ss.company == company)
			& (ss.start_date >= start_date)
			& (ss.end_date <= end_date)
			& (sd.salary_component == salary_component)
		)
		.run()
	)
	total_amt = total_amt and total_amt[0][0] or 0
	return total_amt


@frappe.whitelist()
def get_amount_by_ss_components(company, start_date, end_date, salary_components=[]):
	if isinstance(salary_components, str):
		salary_components = ast.literal_eval(salary_components)
	if not isinstance(salary_components, list):
		salary_components = []
	ss_amount = {}
	for component in salary_components:
		ss_amount[component] = sum_amount_ss_component(
			company, start_date, end_date, component
		)
	return ss_amount