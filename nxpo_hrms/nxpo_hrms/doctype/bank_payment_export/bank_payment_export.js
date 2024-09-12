// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bank Payment Export", {
	refresh(frm) {
		frm.add_custom_button(__("Get Salary Slip"), function () {
			frm.events.get_salary_slip_from_date(frm);
		}).toggleClass("btn-primary", !(frm.doc.bank_sal_slip || []).length);

		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Bank Payment Report"), function () {
				frm.events.go_report(frm);
			}).addClass("btn-primary");
		}
	},

	go_report: function (frm) {
		return frappe
			.call({
				doc: frm.doc,
				method: "get_url_report",
				freeze: true,
				freeze_message: __("Bank Payment Report"),
			})
			.then((r) => {
				window.open(r.message, '_blank');
			});
	},

	get_salary_slip_from_date: function (frm) {
		return frappe
			.call({
				doc: frm.doc,
				method: "fill_sal_slip",
				freeze: true,
				freeze_message: __("Fetching Salary Slip"),
			})
			.then((r) => {
				// console.log('r', r);
				// if (r.docs?.[0]?.custom_payroll_period_employees) {
				frm.dirty();
				// frm.save();
				// }
				frm.refresh();
				frm.scroll_to_field("bank_sal_slip");
			});
	},

});



frappe.ui.form.on("Bank Payment Export Salary Slips", {

	// Triggered when a row is removed from the child table
	bank_sal_slip_remove: function (frm, cdt, cdn) {
		// Calculate the total net pay after a row is removed
		let total_net_pay = frm.doc.bank_sal_slip.reduce((total, row) => {
			return total + (row.net_pay || 0); // Add net_pay values, handle undefined values
		}, 0);

		frm.set_value("total_net_pay",total_net_pay);

	},

});

