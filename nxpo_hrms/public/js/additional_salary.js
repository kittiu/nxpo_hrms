// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Additional Salary", {
	refresh: function (frm) {
		
	},
	from_date: function(frm) {
        // Check if from_date is set
        if (frm.doc.from_date) {

            // Create a date object from the from_date string
            var from_date = new Date(frm.doc.from_date);

            // Add 10 years to the from_date
            from_date.setFullYear(from_date.getFullYear() + 10);

            // Format the new date to YYYY-MM-DD for compatibility with Frappe date fields
            var to_date_ten_years = from_date.toISOString().slice(0, 10);

            // Set the to_date field with the new date
            frm.set_value('to_date', to_date_ten_years);
        }
	}


});
