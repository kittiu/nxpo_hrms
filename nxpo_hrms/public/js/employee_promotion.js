// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Promotion", {
	setup: function(frm) {
		frm.add_fetch("custom_employee_promotion_template", "company", "company");
		frm.add_fetch("custom_employee_promotion_template", "department", "department");
	},

	refresh: function(frm) {
		if (frm.doc.employee) {
			frm.add_custom_button(__('Employee'), function() {
				frappe.set_route("Form", "Employee", frm.doc.employee);
			},__("View"));
		}
		if (frm.doc.custom_project) {
			frm.add_custom_button(__('Project'), function() {
				frappe.set_route("Form", "Project", frm.doc.custom_project);
			},__("View"));
			frm.add_custom_button(__('Task'), function() {
				frappe.set_route('List', 'Task', {project: frm.doc.custom_project});
			},__("View"));
		}
	},

	custom_employee_promotion_template: function(frm) {
		frm.set_value("custom_promotion_activities" ,"");
		if (frm.doc.custom_employee_promotion_template) {
			frappe.call({
				method: "nxpo_hrms.custom.employee_transition.get_transition_details",
				args: {
					"parent": frm.doc.custom_employee_promotion_template,
					"parenttype": "Employee Promotion Template"
				},
				callback: function(r) {
					if (r.message) {
						$.each(r.message, function(i, d) {
							var row = frappe.model.add_child(frm.doc, "Employee Transition Activity", "custom_promotion_activities");
							$.extend(row, d);
						});
					}
					refresh_field("custom_promotion_activities");
				}
			});
		}
	},


	// Overwrite this function to allow only fields used in NXPO
	setup_employee_property_button: function(frm, table) {
		frm.fields_dict[table].grid.add_custom_button(__("Add Employee Property"), () => {
			if (!frm.doc.employee) {
				frappe.msgprint(__("Please select Employee first."));
				return;
			}
			const allowed_fields = [
				{
					label: "Department",
					value: "department",
				},
				{
					label: "Designation",
					value: "designation",
				}
			];
			frappe.model.with_doctype("Employee", () => {
				show_dialog(frm, table, allowed_fields);
			});
		});
	}

});
