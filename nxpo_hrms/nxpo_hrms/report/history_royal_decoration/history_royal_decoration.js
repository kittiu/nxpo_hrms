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
		},
		{
			fieldname: "directorate",
			label: __("Directorate"),
			fieldtype: "Link",
			options: "Department",
			reqd: 0,
		},
		{
			fieldname: "pmu_or_nxpo",
			label: __("PMU or NXPO"),
			fieldtype: "Select",
			options: [
				{ value: "", label: __("Select PMU or NXPO") },
				{ value: "pmu", label: "PMU" },
				{ value: "nxpo", label: "NXPO" },

			],
			reqd: 0,
		},
	],
	onload: function (report) {
		function toggleDirectorateField() {
			let pmu_or_nxpo_value = report.get_values().pmu_or_nxpo;
			let directorate_field = report.page.fields_dict.directorate;
			if (pmu_or_nxpo_value) {
				directorate_field.df.read_only = 1;
			} else {
				directorate_field.df.read_only = 0;
			}
			directorate_field.refresh();
		}

		// Initial toggle based on current value
		toggleDirectorateField();

		// Set up an event listener to handle changes
		report.page.fields_dict.pmu_or_nxpo.$input.on("change", toggleDirectorateField);
	},
};
