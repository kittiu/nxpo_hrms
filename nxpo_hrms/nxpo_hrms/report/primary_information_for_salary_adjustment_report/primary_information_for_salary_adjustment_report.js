// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Primary Information for Salary Adjustment Report"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "fiscal_year",
			label: __("รอบปีงบประมาณ"),
			fieldtype: "Link",
			options: "Fiscal Year",
			reqd: 1,
		},

	]
};
