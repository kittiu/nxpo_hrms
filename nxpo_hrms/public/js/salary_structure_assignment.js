// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Salary Structure Assignment", {
	refresh: function (frm) {
		
	},
	
	employee: function(frm) {
		frm.set_value("custom_confidential_recruitment_type", null);
		frm.set_value("custom_confidential_recruitment_document", null);
		frm.set_value("base", null);
	},

	// Onchange percent -> salary amount
	custom_salary_percent: function(frm) {
		if (frm.doc.custom_salary_percent == 0) { return; }
		if (frm.doc.custom_calculation_method != 'Manual'){
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}
	},
	base: function(frm) {
		if (frm.doc.custom_salary_percent == 0) { return; }
		if (frm.doc.custom_calculation_method != 'Manual'){
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}

	},
	custom_calculation_method: function(frm) {
		if (frm.doc.custom_calculation_method == 'Percent') { 
			frm.set_value(
				"custom_salary_amount",
				parseFloat(frm.doc.custom_salary_percent) / 100 * parseFloat(frm.doc.base)
			);
		}
	},

	custom_confidential_recruitment_type: function(frm) {
		if(frm.doc.custom_confidential_recruitment_type){
			frm.set_query("custom_confidential_recruitment_document", function() {
				return {
					"filters": {
						"type": frm.doc.custom_confidential_recruitment_type,
						"employee": frm.doc.employee
					}
				};
			});
		} else {
			frm.set_value('base', null);
			frm.set_value('custom_confidential_recruitment_document', null);
		}


	},

	custom_confidential_recruitment_document: function(frm) {
        if (frm.doc.custom_confidential_recruitment_document) {
            frappe.db.get_value('Confidential Recruitment Information', frm.doc.custom_confidential_recruitment_document, 'base_salary')
                .then(r => {
                    if (r.message) {
                        frm.set_value('base', r.message.base_salary);
                    }
                });
        }else{
			frm.set_value('base', null);
		}

	},


});
