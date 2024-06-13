// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Salary Structure Assignment", {
	// Onchange percent -> salary amount
	custom_salary_percent: function(frm) {
		if (frm.doc.custom_salary_percent == 0) { return; }
		if (frm.doc.custom_calculation_method != 'Manual'){
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}
	},
	base: function(frm) {
		if (frm.doc.custom_salary_percent == 0) { return; }
		if (frm.doc.custom_calculation_method != 'Manual'){
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}

	},
	custom_calculation_method: function(frm) {
		if (frm.doc.custom_calculation_method == 'Percent') { 
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}
	}
});
