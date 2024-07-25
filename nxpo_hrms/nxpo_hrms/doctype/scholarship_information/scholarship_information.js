// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Scholarship Information", {
	refresh: function (frm) {

	},

    start_date: function(frm) {
		if (frm.doc.end_date) { 
            frappe.call({
                method: "dateOfDuration",
                doc: frm.doc,
                callback: function(response) {
                    frm.set_value('scholarship_duration', response.message);
                }
            });
        }
	},

    end_date: function(frm) {
		if (frm.doc.start_date) { 
            frappe.call({
                method: "dateOfDuration",
                doc: frm.doc,
                callback: function(response) {
                    frm.set_value('scholarship_duration', response.message);
                }
            });        
        }
	},

});
