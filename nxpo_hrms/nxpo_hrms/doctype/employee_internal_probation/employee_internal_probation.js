// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Internal Probation", {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: {
					"status": "Active"
				}
			};
		});
		frm.set_query("probation_department", function (doc) {
			return {
				filters: {
					custom_type: doc.department_type,
				},
			};
		});
	},

	department_type: function(frm) {
		frm.set_value("probation_department", "");
	},


	refresh(frm) {

	},


});
