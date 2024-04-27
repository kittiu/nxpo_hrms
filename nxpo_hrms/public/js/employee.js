// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	onload: function (frm) {
		// Overview HTML
		set_employee_basic_html(frm);
		set_employee_property_history_html(frm);
	},
	setup: function(frm) {
		frm.set_query("custom_subdepartment", function() {
			return {
				filters: {
					custom_type: "กลุ่มงาน"
				}
			};
		});
		frm.set_query("department", function() {
			return {
				filters: {
					custom_type: "ฝ่ายงาน"
				}
			};
		});
		frm.set_query("custom_directorate", function() {
			return {
				filters: {
					custom_type: "แผนกงาน"
				}
			};
		});
	},
	// Onchange 1 remove 2 remove 3
	custom_assignment_designation_1: function(frm) {
		frm.set_value("custom_assignment_department_1", "");
		frm.set_value("custom_assignment_designation_2", "");
	},
	custom_assignment_designation_2: function(frm) {
		frm.set_value("custom_assignment_department_2", "");
		frm.set_value("custom_assignment_designation_3", "");
	},
	custom_assignment_designation_3: function(frm) {
		frm.set_value("custom_assignment_department_3", "");
	},
});

function set_employee_basic_html(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_employee_basic_html",
		args: {
			employee: frm.doc,
		},
		callback: (r) => {
			frm.get_field("custom_summary_html").$wrapper.html(r.message);
		},
	});
}

function set_employee_property_history_html(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_employee_property_history_html",
		args: {
			employee: frm.doc,
		},
		callback: (r) => {
			frm.get_field("custom_property_history_html").$wrapper.html(r.message);
		},
	});
}
