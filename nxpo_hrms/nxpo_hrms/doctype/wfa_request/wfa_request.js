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
                    callback: function() {
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
        // console.log('to_date', row.to_date);
        // console.log('from_date', row.from_date);

        // Calculate the number of days between the dates
        var days_all = moment(row.to_date).diff(row.from_date, "days") + 1;
        
        // Generate the list of dates
        var available_dates = [];
        for (var i = 0; i < days_all; i++) {
            var date = moment(row.from_date).add(i, 'days').format('YYYY-MM-DD');
            available_dates.push(date);
        }

        if(row.from_date && row.to_date){
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Holiday List',
                    filters: {
                        'from_date': ['<=', row.from_date],
                        'to_date': ['>=', row.to_date]
                    },
                    fields: ['name', 'from_date', 'to_date'],
                    order_by:"creation desc",
                    limit_page_length: 1
                },
                callback: function (response) {
                    if(response.message){
                        let holiday_list = response.message[0].name;
                        frappe.call({
                            method: 'nxpo_hrms.custom.holiday.get_holiday_by_parent',
                            args: {
                                parent: holiday_list
                            },
                            callback: function(response) {
                               var holiday_all = response.message
                               if(holiday_all.length > 0){
                                    // Convert arrays to sets for efficient comparison
                                    const available_dates_set = new Set(available_dates);
                                    const holiday_all_set = new Set(holiday_all);
                                    // Find intersection
                                    const matching_dates = Array.from(available_dates_set).filter(date => holiday_all_set.has(date));
                                    // Count matching dates
                                    const matching_count = matching_dates.length;

                                    var days = moment(row.to_date).diff(row.from_date, "days") + 1;
                                    row.days = days - matching_count
                                    refresh_field("plan_dates")
                               }else{
                                    var days = moment(row.to_date).diff(row.from_date, "days") + 1;
                                    row.days = days
                                    refresh_field("plan_dates")
                               }
 
                            }
                        });
                    }else{
                        row.days = moment(row.to_date).diff(row.from_date, "days") + 1
                        refresh_field("plan_dates")
                    }

            
                }
            });

        }

    },
    to_date: function (frm, cdt, cdn) {

        var row = locals[cdt][cdn];
        // Calculate the number of days between the dates
        var days_all = moment(row.to_date).diff(row.from_date, "days") + 1;
        
        // Generate the list of dates
        var available_dates = [];
        for (var i = 0; i < days_all; i++) {
            var date = moment(row.from_date).add(i, 'days').format('YYYY-MM-DD');
            available_dates.push(date);
        }

        if(row.from_date && row.to_date){

            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Holiday List',
                    filters: {
                        'from_date': ['<=', row.from_date],
                        'to_date': ['>=', row.to_date]
                    },
                    fields: ['name', 'from_date', 'to_date'],
                    order_by:"creation desc",
                    limit_page_length: 1
                },
                callback: function (response) {
                    if(response.message){
                        let holiday_list = response.message[0].name;
                        frappe.call({
                            method: 'nxpo_hrms.custom.holiday.get_holiday_by_parent',
                            args: {
                                parent: holiday_list
                            },
                            callback: function(response) {
                               var holiday_all = response.message
                               if(holiday_all.length > 0){
                                    // Convert arrays to sets for efficient comparison
                                    const available_dates_set = new Set(available_dates);
                                    const holiday_all_set = new Set(holiday_all);
                                    // Find intersection
                                    const matching_dates = Array.from(available_dates_set).filter(date => holiday_all_set.has(date));
                                    // Count matching dates
                                    const matching_count = matching_dates.length;

                                    var days = moment(row.to_date).diff(row.from_date, "days") + 1;
                                    row.days = days - matching_count
                                    refresh_field("plan_dates")
                               }else{
                                    var days = moment(row.to_date).diff(row.from_date, "days") + 1;
                                    row.days = days
                                    refresh_field("plan_dates")
                               }
 
                            }
                        });
                    }else{
                        row.days = moment(row.to_date).diff(row.from_date, "days") + 1
                        refresh_field("plan_dates")
                    }

            
                }
            });

        }


        refresh_field("plan_dates")
    },

});
