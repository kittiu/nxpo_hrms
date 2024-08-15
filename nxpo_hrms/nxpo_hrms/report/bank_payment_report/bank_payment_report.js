// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Bank Payment Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "date",
			label: __("Date"),
			fieldtype: "Date",
			reqd: 1,
            // default: frappe.datetime.month_start(),
		},
		// {
		// 	fieldname: "date_for_split_tax",
		// 	label: __("Date For Split Tax"),
		// 	fieldtype: "Date",
		// 	reqd: 1,
        //     // default: frappe.datetime.month_end(),
		// },
		{
			fieldname: "docstatus",
			label: __("Document Status"),
			fieldtype: "Select",
			options: [
                {value: 0, label: "Draft"},
                {value: 1, label: "Submitted"},
                {value: 2, label: "Cancelled"},
            ],
			default: 1,
			reqd: 1,
		},
		{
			fieldname: "nob",
			label: __("Normal or Bonus"),
			fieldtype: "Select",
			options: [
                {value: 'normal', label: "Normal"},
                {value: 'bonus', label: "Bonus"},
            ],
			default: 'normal',
			reqd: 1,
		},
	]
};
