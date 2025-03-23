// Turn off existing function
// frappe.ui.form.off("Leave Application", "make_dashboard");
// Turn on new function
frappe.ui.form.on("Leave Application", {

	half_day: function (frm) {
		frm.set_value("custom_hours", "4");
	},

	// make_dashboard: function (frm) {
	// 	let leave_details;
	// 	let lwps;

	// 	if (frm.doc.employee) {
	// 		frappe.call({
	// 			method: "hrms.hr.doctype.leave_application.leave_application.get_leave_details",
	// 			async: false,
	// 			args: {
	// 				employee: frm.doc.employee,
	// 				date: frm.doc.from_date || frm.doc.posting_date,
	// 			},
	// 			callback: function (r) {
	// 				if (!r.exc && r.message["leave_allocation"]) {
	// 					leave_details = r.message["leave_allocation"];
	// 				}
	// 				lwps = r.message["lwps"];
	// 			},
	// 		});

	// 		$("div").remove(".form-dashboard-section.custom");

	// 		frm.dashboard.add_section(
	// 			frappe.render_template("nxpo_leave_application_dashboard", {
	// 				data: leave_details,
	// 			}),
	// 			__("Allocated Leaves"),
	// 		);
	// 		frm.dashboard.show();

	// 		let allowed_leave_types = Object.keys(leave_details);
	// 		// lwps should be allowed for selection as they don't have any allocation
	// 		allowed_leave_types = allowed_leave_types.concat(lwps);

	// 		frm.set_query("leave_type", function () {
	// 			return {
	// 				filters: [["leave_type_name", "in", allowed_leave_types]],
	// 			};
	// 		});
	// 	}
	// },

});
