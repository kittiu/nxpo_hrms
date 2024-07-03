// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Allocation", {
	refresh: function (frm) {
		if (frm.doc.carry_forward) {
			frm.toggle_display("custom_add_unused_leave", false);
			frm.toggle_display("custom_total_unused_leave", false);
		}else{
			if (frm.doc.custom_is_add_unused_leave) {
				// frm.set_df_property('custom_add_unused_leave', "read_only", 1);
				frm.toggle_display("custom_add_unused_leave", false);
				frm.toggle_display("custom_cancel_unused_leave", true);
			}else{
				frm.toggle_display("custom_add_unused_leave", true);
				frm.toggle_display("custom_cancel_unused_leave", false);
			}
		}

	},

	custom_add_unused_leave: function(frm) {
		if (!frm.doc.custom_is_add_unused_leave) {
			frm.call({
				doc: frm.doc,
				method: 'get_leave_ledger',
				args: {
					data: frm.doc
				},
				callback: function(response) {
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
	custom_cancel_unused_leave: function(frm) {
		if (frm.doc.custom_is_add_unused_leave) {
			frm.set_value('custom_total_unused_leave', 0)
			frm.set_value('total_leaves_allocated', frm.doc.new_leaves_allocated)
			frm.set_value('custom_is_add_unused_leave', 0)
			frm.save('Update');
		}
	}

});
