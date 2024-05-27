// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Org Structure", {
	setup: function (frm) {
        for (let field of ["level_1", "level_2", "level_3", "level_4"]) {
            frm.set_query(field, "items", function (doc, cdt, cdn) {
                var item = locals[cdt][cdn];
                return {
                    query: "nxpo_hrms.nxpo_hrms.doctype.org_structure.org_structure.get_departments",
                    filters: {
                        company: doc.company,
                        custom_type: item.type,
                    },
                };
            });
        }
	},
    refresh: function (frm) {
        if (frm.doc.docstatus == 0) {
            msg = "<strong>Warning:</strong> By submit this document, the Org Structure will be applied which will enable/disable departments accordingly."
            frm.dashboard.add_comment(msg, "yellow", true);
        }
    }
});

frappe.ui.form.on("Org Structure Tree", {
	type: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        row.level_1 = row.level_2 = row.level_3 = null;
        refresh_field("items");
	},
});

