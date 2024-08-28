frappe.listview_settings["Employee Tax Exemption Declaration"] = {
	onload: function (listview) {
		listview.page.add_menu_item(__("Email Employee Tax Exemption Declaration"), () => {
			// console.log(listview.get_checked_items(), 'Employee Tax');

			if (!listview.get_checked_items().length) {
				frappe.msgprint(__("Please select "));
				return;
			}

			frappe.confirm(__("Are you sure you want to email the selected employee tax exemption declaration?"), () => {
				listview.call_for_selected_items(
					"nxpo_hrms.custom.employee_tax_exemption_declaration.enqueue_email_employee_tax_exemption_declaration",
				);
			});
		});
	},
};
