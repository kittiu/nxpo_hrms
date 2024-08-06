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
		{
			fieldname: "pmu_or_nxpo",
			label: __("PMU or NXPO"),
			fieldtype: "Select",
			options: [
				{value: "", label: __("Select PMU or NXPO")},
				{value: "pmu", label: "PMU"},
				{value: "nxpo", label: "NXPO"},
        
            ],
			reqd: 0,
		},
	],
    onload: function(report) {
        function toggleDirectorateField() {
            let pmu_or_nxpo_value = report.get_values().pmu_or_nxpo;
            let directorate_field = report.page.fields_dict.directorate;
            directorate_field.df.read_only = !!pmu_or_nxpo_value;
            directorate_field.refresh();
        }

        // Initial toggle based on current value
        toggleDirectorateField();

        // Set up an event listener to handle changes
        report.page.fields_dict.pmu_or_nxpo.$input.on("change", toggleDirectorateField);
    },
};
