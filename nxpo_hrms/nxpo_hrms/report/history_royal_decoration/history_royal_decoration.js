// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["History Royal Decoration"] = {
	"filters": [
		{
			fieldname: "year",
			fieldtype: "Link",
			label: "Year",
			options: "Fiscal Year",
			reqd: 0,
		},
		{
			fieldname: "employee",
			fieldtype: "Link",
			label: "Employee",
			options: "Employee",
		}
	]
};
