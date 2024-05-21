# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import frappe
from frappe.utils import get_fullname


@frappe.whitelist()
def get_my_documents_config():
	return {
		"Salary Slip": {
			"fields": [
				{"fieldname": "posting_date", "fieldtype": "Date"},
				{"fieldname": "gross_pay", "fieldtype": "Currency"},
				{"fieldname": "total_deduction", "fieldtype": "Currency"},
				{"fieldname": "gross_year_to_date", "fieldtype": "Currency"},
			],
			"method": "nxpo_hrms.nxpo_hrms.page.my_documents.my_documents.get_salary_slips",
			"company_disabled": 1,
			"icon": "income",
			"menu_name": "Salary Slip",
		},
		"Withholding Tax Cert Employee": {
			"fields": [
				{"fieldname": "date", "fieldtype": "Date"}
			],
			"method": "nxpo_hrms.nxpo_hrms.page.my_documents.my_documents.get_wht_cert_employee",
			"company_disabled": 1,
			"icon": "file",
			"menu_name": "Witholding Tax Cert"

		}
	}


@frappe.whitelist()
def get_salary_slips(date_range, company=None, field=None, employee=None, limit=None):

	filters = [["docstatus", "=", 1]]
	if date_range:
		date_range = frappe.parse_json(date_range)
		filters.append(["posting_date", "between", [date_range[0], date_range[1]]])
	if employee:
		filters.append(["employee", "=", employee])

	select_field = "{} as value".format(field)

	salary_slips = frappe.get_list(
		doctype="Salary Slip",
		fields=["name", select_field, "employee_name"],
		filters=filters
	)

	for ss in salary_slips:
		ss["formatted_name"] = f'<a href="/app/print/Salary Slip/{ss["name"]}">{ss["name"]}</a>'

	return salary_slips


@frappe.whitelist()
def get_wht_cert_employee(date_range, company=None, field=None, employee=None, limit=None):

	filters = [["docstatus", "=", 1]]
	if date_range:
		date_range = frappe.parse_json(date_range)
		filters.append(["date", "between", [date_range[0], date_range[1]]])
	if employee:
		filters.append(["employee", "=", employee])

	select_field = "{} as value".format(field)

	salary_slips = frappe.get_list(
		doctype="Withholding Tax Cert Employee",
		fields=["name", select_field, "employee_name"],
		filters=filters
	)

	for ss in salary_slips:
		ss["formatted_name"] = f'<a href="/app/print/Withholding Tax Cert Employee/{ss["name"]}">{ss["name"]}</a>'

	return salary_slips
