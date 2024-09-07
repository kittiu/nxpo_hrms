// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bank Payment Export", {
	refresh(frm) {
		frm.add_custom_button(__("Get Salary Slip"), function () {
			frm.events.get_salary_slip_from_date(frm);
		}).toggleClass("btn-primary", !(frm.doc.bank_sal_slip || []).length);
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


