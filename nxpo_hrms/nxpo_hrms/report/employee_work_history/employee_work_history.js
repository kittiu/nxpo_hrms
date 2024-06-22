// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Work History"] = {
	filters: [
		{
			fieldname: "directorate",
			label: __("Directorate"),
			fieldtype: "MultiSelectList",
			options: "Department",
			get_data: function (txt) {
				return frappe.db.get_link_options("Department", txt, {
					custom_type: "กลุ่มงาน"
				});
			},
		},
		{
			fieldname: "internal",
			label: __("Internal Work"),
			fieldtype: "Check",
			default: 1,
		},
		{
			fieldname: "external",
			label: __("External Work"),
			fieldtype: "Check",
			default: 1,
		},
		{
			fieldname: "ease_viewing",
			label: __("Ease Viewing"),
			fieldtype: "Check",
			default: 1,
		},
	],
};
