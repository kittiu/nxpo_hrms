// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Scholarship Information", {
    refresh: function (frm) {
        if (frm.doc.type_of_information === 'พนักงาน') {
            frm.set_df_property('other_prefix', 'hidden', 1);
            frm.set_df_property('employee', 'hidden', 0);
            frm.set_df_property('prefix', 'hidden', 0);
            frm.set_df_property('full_name', 'read_only', 1);  // Keep it read-only for 'พนักงาน'
        } else if (frm.doc.type_of_information === 'บุคคลภายนอก') {
            frm.set_df_property('employee', 'hidden', 1);
            frm.set_df_property('prefix', 'hidden', 1);
            frm.set_df_property('other_prefix', 'hidden', 0);
            frm.set_df_property('full_name', 'read_only', 0);  // Make it editable
            frm.refresh_field('full_name');
        }
        frm.refresh_field('full_name'); // Refresh the field to ensure the UI updates
    },

    type_of_information: function (frm) {
        frm.trigger('refresh');
        frm.set_value('prefix', null);
        frm.set_value('full_name', null);
        frm.set_value('employee', null);
    
    },
    employee: function (frm) {

        // Get the employee ID from the form
        const employee_id = frm.doc.employee;
        // Check if employee_id is available
        if (employee_id && frm.doc.type_of_information === 'พนักงาน') {
            // Fetch the full_name from the Employee doctype
            frappe.db.get_value('Employee', employee_id, 'employee_name', function (value) {
                if (value && value.employee_name) {
                    frm.set_value('full_name', value.employee_name);
                } else {
                    frappe.msgprint(__('Full name not found for the selected employee.'));
                }
            });
        }
    },
    start_date: function (frm) {
        if (frm.doc.end_date) {
            frappe.call({
                method: "get_diff_date_duration",
                doc: frm.doc,
                callback: function (response) {
                    frm.set_value('scholarship_duration', response.message);
                }
            });
        }
    },

    end_date: function (frm) {
        if (frm.doc.start_date) {
            frappe.call({
                method: "get_diff_date_duration",
                doc: frm.doc,
                callback: function (response) {
                    frm.set_value('scholarship_duration', response.message);
                }
            });
        }
    },

});
