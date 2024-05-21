// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee Bulk Transfer", {

// 	refresh: function (frm) {
// 		// if (frm.doc.status === "Queued") frm.page.btn_secondary.hide()

// 		if (frm.doc.docstatus === 0 && !frm.is_new()) {
// 			frm.page.clear_primary_action();
// 			frm.add_custom_button(__("Get Employees"),
// 				function() {
// 					frm.events.get_employee_details(frm);
// 				}
// 			).toggleClass("btn-primary", !(frm.doc.employees || []).length);
// 		}

// 		if (
// 			(frm.doc.employees || []).length
// 			&& !frappe.model.has_workflow(frm.doctype)
// 			&& !cint(frm.doc.employee_transfers_created)
// 			&& (frm.doc.docstatus != 2)
// 		) {
// 			if (frm.doc.docstatus == 0 && !frm.is_new()) {
// 				frm.page.clear_primary_action();
// 				frm.page.set_primary_action(__("Create Employee Transfers"), () => {
// 					frm.save("Submit").then(() => {
// 						frm.page.clear_primary_action();
// 						frm.refresh();
// 					});
// 				});
// 			} else if (frm.doc.docstatus == 1 && frm.doc.status == "Failed") {
// 				frm.add_custom_button(__("Create Employee Transfers"), function () {
// 					frm.call("create_employe_transfers");
// 				}).addClass("btn-primary");
// 			}
// 		}

// 		if (frm.doc.docstatus == 1) {
// 			if (frm.custom_buttons) frm.clear_custom_buttons();
// 			frm.events.add_context_buttons(frm);
// 		}

// 		if (frm.doc.status == "Failed" && frm.doc.error_message) {
// 			const issue = `<a id="jump_to_error" style="text-decoration: underline;">issue</a>`;
// 			let process = (cint(frm.doc.employee_transfers_created)) ? "submission" : "creation";

// 			frm.dashboard.set_headline(
// 				__("Employee Transfer {0} failed. You can resolve the {1} and retry {0}.", [process, issue])
// 			);

// 			$("#jump_to_error").on("click", (e) => {
// 				e.preventDefault();
// 				frm.scroll_to_field("error_message");
// 			});
// 		}
// 	},

// 	get_employee_details: function (frm) {
// 		return frappe.call({
// 			doc: frm.doc,
// 			method: 'fill_employee_details',
// 			freeze: true,
// 			freeze_message: __('Fetching Employees')
// 		}).then(r => {
// 			if (r.docs?.[0]?.employees) {
// 				frm.dirty();
// 				frm.save();
// 			}

// 			frm.refresh();

// 			if (r.docs?.[0]?.validate_attendance) {
// 				render_employee_attendance(frm, r.message);
// 			}
// 			frm.scroll_to_field("employees");
// 		});
// 	},

// 	create_employee_transfers: function (frm) {
// 		frm.call({
// 			doc: frm.doc,
// 			method: "run_doc_method",
// 			args: {
// 				method: "create_employee_transfers",
// 				dt: "Employee Bulk Transfer",
// 				dn: frm.doc.name
// 			}
// 		});
// 	},

// 	add_context_buttons: function (frm) {
// 		// if (frm.doc.employee_transfers_submitted || (frm.doc.__onload && frm.doc.__onload.submitted_ss)) {
// 		// 	frm.events.add_bank_entry_button(frm);
// 		// } else if (frm.doc.employee_transfers_created && frm.doc.status !== "Queued") {
// 		if (frm.doc.employee_transfers_created && frm.doc.status !== "Queued") {
//             frm.add_custom_button(__("Submit Employee Transfers"), function() {
// 				submit_employee_transfer(frm);
// 			}).addClass("btn-primary");
// 		} else if (!frm.doc.employee_transfers_created && frm.doc.status === "Failed") {
// 			frm.add_custom_button(__("Create Employee Transfers"), function() {
// 				frm.trigger("create_employee_transfers");
// 			}).addClass("btn-primary");
// 		}
// 	},
// });

// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Bulk Transfer", {
	onload: function (frm) {
		set_html_data(frm);
	},
});

function set_html_data(frm) {
    frm.get_field("html_vlqa").$wrapper.html('<b>XXX</b>YYY');
	// if (frm.doc.docstatus === 1 && frm.doc.status == "Submitted") {
	// 	frappe.call({
	// 		method: "get_payment_reconciliation_details",
	// 		doc: frm.doc,
	// 		callback: (r) => {
	// 			frm.get_field("payment_reconciliation_details").$wrapper.html(r.message);
	// 		},
	// 	});
	// }
}

