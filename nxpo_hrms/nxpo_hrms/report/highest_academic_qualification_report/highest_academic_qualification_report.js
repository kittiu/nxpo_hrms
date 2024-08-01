// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Highest Academic Qualification Report"] = {
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
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 0,
		},
		{
			fieldname: "degree",
			label: __("Highest Degree"),
			fieldtype: "Select",
			options: [
                {value: '', label: ""},
                {value: 'ปริญญาตรี', label: "ปริญญาตรี"},
                {value: 'ปริญญาโท', label: "ปริญญาโท"},
				{value: 'ปริญญาเอก', label: "ปริญญาเอก"},
            ],
			reqd: 0,
		},
	]
};
