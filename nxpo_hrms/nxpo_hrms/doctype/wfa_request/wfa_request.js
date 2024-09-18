// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("WFA Request", {

    refresh: function (frm) {
        // hide [+] button from linked document
        $('[data-doctype="Attendance Request"]').find("button").hide();
        // Add View Attendances button
        if (!frm.doc.__islocal) {
            frm.events.add_view_attendance_button(frm);
        }
        // Add context button
        if (frm.doc.docstatus == 1) {
            frm.events.add_create_attendance_button(frm);
        }
    },

    // Onchange field Type will change field Development to null
    type: function (frm) {
        frm.set_value("development", null)
    },

    // employee: async function (frm) {
    //     if (frm.doc.employee) {
    //         let e = await frappe.db.get_doc("Employee", frm.doc.employee)
    //         if (e && e.leave_approver) {  // Leave Approver from Employee
    //             frm.set_value("approver", e.leave_approver)
    //         } else if (e.department) {  // Leave Approver from Department
    //             let d = await frappe.db.get_doc("Department", e.department)
    //             if (d && d.leave_approvers.length) {
    //                 frm.set_value("approver", d.leave_approvers[0]["approver"])
    //             }
    //         } else {
    //             frm.set_value("approver", null) 
    //         }
    //     } else {
    //         frm.set_value("approver", null)
    //     }
    // },

    add_view_attendance_button: function (frm) {
        frappe.db.get_list("Attendance Request", {
            filters: { custom_wfa_request: frm.doc.name },
            fields: ["name"]
        }).then((res) => {
            let requests = [];
            res.forEach((request) => {
                requests.push(request.name);
            });
            if (requests && requests.length) {
                frm.add_custom_button(__("View All WFA Attendances"), function () {
                    frappe.set_route("List", "Attendance", { attendance_request: ["in", requests] });
                });
            }
        })
    },

    add_create_attendance_button: function (frm) {
        if (frm.doc.status !== "Completed") {
            frm.add_custom_button(__("Create Attendance"), function () {
                frappe.call({
                    method: "create_attendance_requests",
                    doc: frm.doc,
                    callback: function () {
                        frm.reload_doc();
                    }
                });
            }).addClass("btn-primary");
        }
    },
});


frappe.ui.form.on("WFA Request Line", {

    from_date: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        row.to_date = row.from_date
        let company = frappe.defaults.get_default("company");

        if (row.from_date && row.to_date) {

            frappe.db.get_value('Company', company, 'default_holiday_list', function (value) {
                if (value && value.default_holiday_list) {
                    let holiday_list = value.default_holiday_list;
                    frappe.call({
                        method: "get_number_of_leave_days_for_wfa",
                        doc: frm.doc,
                        args: {
                            from_date: row.from_date,
                            to_date: row.to_date,
                            employee: frm.doc.employee,
                            holiday_list: holiday_list
                        },
                        callback: function (response) {
                            var holiday_result = response.message
                            row.days = holiday_result
                            refresh_field("plan_dates")
                        }
                    });
                    frappe.call({
                        method: "get_sum_total_days",
                        doc: frm.doc,
                        args: {
                            holiday_list: holiday_list
                        },
                        callback: function (response) {
                            var total_day = response.message
                            frm.set_value("total_days", total_day)
                            frm.refresh_field("total_days"); 
                        }
                    });

                } else {
                    row.days = moment(row.to_date).diff(row.from_date, "days") + 1
                    refresh_field("plan_dates")
                }
            });

        }

    },
    to_date: function (frm, cdt, cdn) {

        var row = locals[cdt][cdn];
        let company = frappe.defaults.get_default("company");

        if (row.from_date && row.to_date) {
            
            frappe.db.get_value('Company', company, 'default_holiday_list', function (value) {
                if (value && value.default_holiday_list) {
                    let holiday_list = value.default_holiday_list;

                    frappe.call({
                        method: "get_number_of_leave_days_for_wfa",
                        doc: frm.doc,
                        args: {
                            from_date: row.from_date,
                            to_date: row.to_date,
                            employee: frm.doc.employee,
                            holiday_list: holiday_list
                        },
                        callback: function (response) {
                            var holiday_result = response.message
                            row.days = holiday_result
                            refresh_field("plan_dates")
                        }
                    });

                    frappe.call({
                        method: "get_sum_total_days",
                        doc: frm.doc,
                        args: {
                            holiday_list: holiday_list
                        },
                        callback: function (response) {
                            var total_day = response.message
                            frm.set_value("total_days", total_day)
                            frm.refresh_field("total_days"); 
                        }
                    });

                } else {
                    row.days = moment(row.to_date).diff(row.from_date, "days") + 1
                    refresh_field("plan_dates")
                }
            });




        }
    },

});
