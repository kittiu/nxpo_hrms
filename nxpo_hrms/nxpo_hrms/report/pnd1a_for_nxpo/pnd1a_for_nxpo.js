// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["PND1a For NXPO"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			width: "100px",
			reqd: 1,
		},
		{
			fieldname: "payroll_period",
			label: __("Payroll Period"),
			fieldtype: "Link",
			options: "Payroll Period",
			reqd: 1,
			on_change: () => {
				var period = frappe.query_report.get_filter_value("payroll_period");
				if (period) {
					frappe.db.get_value("Payroll Period", period, ["start_date", "end_date"], function (value) {
						frappe.query_report.set_filter_value("from_date", value["start_date"]);
						frappe.query_report.set_filter_value("to_date", value["end_date"]);
					});
				} else {
					frappe.query_report.set_filter_value("from_date", "");
					frappe.query_report.set_filter_value("to_date", "");
				}
			},
		},
		{
			fieldname: "from_date",
			label: __("From"),
			fieldtype: "Date",
			reqd: 1,
			width: "100px",
		},
		{
			fieldname: "to_date",
			label: __("To"),
			fieldtype: "Date",
			reqd: 1,
			width: "100px",
		},
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
