// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Allocation", {
	refresh: function (frm) {
		if (frm.doc.carry_forward || frm.is_new()) {
			frm.toggle_display("custom_add_unused_leave", false);
			frm.toggle_display("custom_total_unused_leave", false);
		} else {
			if (frm.doc.custom_is_add_unused_leave) {
				frm.toggle_display("custom_add_unused_leave", false);
				frm.toggle_display("custom_cancel_unused_leave", true);
			} else {
				frm.toggle_display("custom_add_unused_leave", true);
				frm.toggle_display("custom_cancel_unused_leave", false);
			}
		}

	},

	custom_add_unused_leave: function (frm) {
		if (!frm.doc.custom_is_add_unused_leave && frm.doc.from_date && frm.doc.to_date && frm.doc.employee && frm.doc.leave_type) {
			frm.call({
				method: 'nxpo_hrms.custom.leave_allocation.get_unused_leave',
				args: {
					data: frm.doc
				},
				callback: function (response) {
					if (response.message) {
						const total_unused_leave = response.message
						const sumLeave = total_unused_leave + frm.doc.new_leaves_allocated
						frm.set_value('custom_total_unused_leave', total_unused_leave)
						frm.set_value('total_leaves_allocated', sumLeave)
						frm.set_value('custom_is_add_unused_leave', 1)
						frm.save('Update');
					}
				}
			});
		}

	},
	custom_cancel_unused_leave: function (frm) {
		if (frm.doc.custom_is_add_unused_leave && frm.doc.from_date && frm.doc.to_date && frm.doc.employee && frm.doc.leave_type) {
			frm.set_value('custom_total_unused_leave', 0)
			frm.set_value('total_leaves_allocated', frm.doc.new_leaves_allocated)
			frm.set_value('custom_is_add_unused_leave', 0)
			frm.save('Update');
		}
	}

});

frappe.listview_settings['Leave Allocation'] = {
	onload: function (listview) {
		listview.page.add_action_item(__('Add unused leave'), function () {
			// Get selected items
			let selected_items = listview.get_checked_items();

			// Ensure there are selected items
			if (selected_items.length === 0) {
				frappe.msgprint(__('Please select at least one item.'));
				return;
			}
			 // Extract names of selected items
            var list_names = selected_items.map(item => item.name);

            // Call server-side method
            frappe.call({
                method: 'nxpo_hrms.custom.leave_allocation.update_leave_allocation_unused_leave', // Replace with the actual path
                args: {
                    names: list_names,
                    action: 'add_unused_leave'
                },
                callback: function(response) {
                    if (!response.exc) {
                        frappe.msgprint(__('Add unused leave completed.'));
                        listview.refresh(); // Refresh the list view after the update
                    } else {
                        console.error('Failed to update records:', response.exc);
                        frappe.msgprint(__('Failed to update records.'));
                    }
                }
            });

		});

		listview.page.add_action_item(__('Cancel unused leave'), function () {
			// Get selected items
			let selected_items = listview.get_checked_items();

			// Ensure there are selected items
			if (selected_items.length === 0) {
				frappe.msgprint(__('Please select at least one item.'));
				return;
			}
			 // Extract names of selected items
            var list_names = selected_items.map(item => item.name);

            // Call server-side method
            frappe.call({
                method: 'nxpo_hrms.custom.leave_allocation.update_leave_allocation_unused_leave', // Replace with the actual path
                args: {
                    names: list_names,
                    action: 'cancel_unused_leave'
                },
                callback: function(response) {
                    if (!response.exc) {
                        frappe.msgprint(__('Cancel unused leave completed.'));
                        listview.refresh(); // Refresh the list view after the update
                    } else {
                        console.error('Failed to update records:', response.exc);
                        frappe.msgprint(__('Failed to update records.'));
                    }
                }
            });

		});
	}
}
