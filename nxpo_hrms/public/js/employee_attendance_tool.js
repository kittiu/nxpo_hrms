frappe.ui.form.on("Employee Attendance Tool", {

	show_marked_employees(frm, marked_employees) {
		const $wrapper = frm.get_field("marked_attendance_html").$wrapper;
		const summary_wrapper = $(`<div class="summary_wrapper">`).appendTo($wrapper);
		const data = marked_employees.map((entry) => {
			// return [`${entry.employee} : ${entry.employee_name}`, entry.status];
			return [`${entry.employee} : ${entry.employee_name}`, entry.status, entry.custom_work_from_anywhere];
		});
		console.log(data)
		frm.events.render_datatable(frm, data, summary_wrapper);
	},

	get_columns_for_marked_attendance_table(frm) {
		return [
			{
				name: "employee",
				id: "employee",
				content: __("Employee"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 350,
			},
			{
				name: "status",
				id: "status",
				content: __("Status"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 150,
				format: (value) => {
					if (value == "Present" || value == "Work From Home")
						return `<span style="color:green">${__(value)}</span>`;
					else if (value == "Absent")
						return `<span style="color:red">${__(value)}</span>`;
					else if (value == "Half Day")
						return `<span style="color:orange">${__(value)}</span>`;
					else if (value == "On Leave")
						return `<span style="color:#318AD8">${__(value)}</span>`;
				},
			},
			// Additional field
			{
				name: "work_from_anywhere",
				id: "work_from_anywhere",
				content: __("WFA"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 20,
				format: (value) => {
					if (value == "1")
						return "✔";
					else
						return "";
				},
			},
			// --
		];
	},

});
