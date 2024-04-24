// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	onload: function (frm) {
		set_employee_basic_html(frm);
		set_employee_property_history_html(frm);
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
