// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	refresh: function (frm) {
		// Change label of a field name using jquery
		$("[data-fieldname='__newname']").find("label").text("Employee ID");
	},
	onload: function (frm) {
		// Overview HTML
		set_employee_basic_html(frm);
		set_employee_transition_html(frm);
		set_employee_special_assignment(frm);
		set_external_work_html(frm);
		set_education_html(frm);
	},
	setup: function(frm) {
		frm.set_query("custom_subdepartment", function() {
			return {
				filters: {
					custom_type: "แผนกงาน"
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
					custom_type: "กลุ่มงาน"
				}
			};
		});
		frm.set_query('custom_bank_branch', function() {
            return {
                filters: [
                    ['Bank Branch', 'bank', '=', frm.doc.custom_bank]
                ]
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
	// relieving_date = custom_exit_effective_date + 1
	custom_exit_effective_date: function(frm) {
		var exit_date = frm.doc.custom_exit_effective_date;
		var relieving_date = frappe.datetime.add_days(exit_date, -1);
		frm.set_value("relieving_date", relieving_date);
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

function set_employee_transition_html(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_employee_transition_html",
		args: {
			employee: frm.doc.name,
		},
		callback: (r) => {
			console.log(r.message)
			frm.get_field("custom_employee_transition_html").$wrapper.html(r.message);
		},
	});
}

function set_external_work_html(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_external_work_html",
		args: {
			employee: frm.doc.name,
		},
		callback: (r) => {
			console.log(r.message)
			frm.get_field("custom_external_work_html").$wrapper.html(r.message);
		},
	});
}

function set_education_html(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_education_html",
		args: {
			employee: frm.doc.name,
		},
		callback: (r) => {
			console.log(r.message)
			frm.get_field("custom_education_html").$wrapper.html(r.message);
		},
	});
}

function set_employee_special_assignment(frm) {
	frappe.call({
		method: "nxpo_hrms.custom.employee.get_employee_special_assignment",
		args: {
			employee: frm.doc.name,
		},
		callback: (r) => {
			console.log(r.message)
			frm.get_field("custom_employee_special_assignment_html").$wrapper.html(r.message);
		},
	});
}

