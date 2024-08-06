frappe.query_reports["Payroll Report"] = {
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
			fieldname: "status_emp",
			label: __("Employee Status"),
			fieldtype: "Select",
			options: [
				{value: "", label: __("Select Employee Status")},
                {value: "Active", label: "Active"},
                {value: "Inactive", label: "Inactive"},
                {value: "Suspended", label: "Suspended"},
				{value: "Left", label: "Left"},
            ],
			reqd: 0,
		},
		{
			fieldname: "directorate",
			label: __("Directorate"),
			fieldtype: "Link",
			options: "Department",
			reqd: 0,
		},
		{
			fieldname: "employment_type",
			label: __("ประเภทพนักงาน"),
			fieldtype: "Link",
			options: "Employment Type",
			reqd: 0,
		},
		{
			fieldname: "posting_date",
			label: __("Posting Date"),
			fieldtype: "Date",
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

    formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname.includes(__("percentile"))) {
			if (data[column.fieldname] < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			} else if (data[column.fieldname] > 0) {
				value = "<span style='color:green'>" + value + "</span>";
			}
		}
		return value;
	},
};
