frappe.listview_settings['Employee Transfer'] = {
	add_fields: ["custom_transition_status"],
	get_indicator: function(doc) {
		return [__(doc.custom_transition_status), frappe.utils.guess_colour(doc.custom_transition_status), "status,=," + doc.custom_transition_status];
	}
};
