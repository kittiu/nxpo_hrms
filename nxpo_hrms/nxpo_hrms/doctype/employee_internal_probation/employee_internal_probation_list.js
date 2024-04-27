frappe.listview_settings["Employee Internal Probation"] = {
	has_indicator_for_draft: 1,
	get_indicator: function(doc) {
		let status_color = {
			"Pending": "orange",
			"Under Probation": "blue",
			"Pass": "green",
			"Not Pass": 'red',
		};
		return [__(doc.status), status_color[doc.status], 'status,=,'+doc.status];
	}
};

