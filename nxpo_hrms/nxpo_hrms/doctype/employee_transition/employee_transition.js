// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Transition", {
	refresh(frm) {
        frm.set_query("designation", function(){
            return {
                filters: {
                    "disabled": 0
                }
            }
        });
	},


});
