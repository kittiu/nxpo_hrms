// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Attendance Report"] = {
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
			fieldname: "employee_f",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 0,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
            default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
            default: frappe.datetime.month_end(),
		},
		{
			fieldname: "atd_status",
			label: __("Status"),
			fieldtype: "Select",
			options: [
                {value: "", label: ""},
                {value: "Present", label: "Present"},
                {value: "Absent", label: "Absent"},
				{value: "On Leave", label: "On Leave"},
				{value: "Half Day", label: "Half Day"},
            ],
			reqd: 0,
		},
		{
			fieldname: "is_owr",
			label: __("Work From Anywhere"),
			fieldtype: "Check",
			reqd: 0,
		},
	],
};
