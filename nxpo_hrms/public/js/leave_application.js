frappe.ui.form.on("Leave Application", {

	refresh: function (frm) {

	},

    calculate_total_days: function (frm) {

        var days_all = moment(frm.doc.to_date).diff(frm.doc.from_date, "days") + 1;

        // Generate the list of dates
        var available_dates = [];
        for (var i = 0; i < days_all; i++) {
            var date = moment(frm.doc.from_date).add(i, 'days').format('YYYY-MM-DD');
            available_dates.push(date);
        }
        var days = moment(frm.doc.to_date).diff(frm.doc.from_date, "days") + 1;

        if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee && frm.doc.leave_type) {

            // // server call is done to include holidays in leave days calculations
            // return frappe.call({
            //     method: "hrms.hr.doctype.leave_application.leave_application.get_number_of_leave_days",
            //     args: {
            //         employee: frm.doc.employee,
            //         leave_type: frm.doc.leave_type,
            //         from_date: frm.doc.from_date,
            //         to_date: frm.doc.to_date,
            //         half_day: frm.doc.half_day,
            //         half_day_date: frm.doc.half_day_date,
            //     },
            //     callback: function (r) {
            //         if (r && r.message) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Holiday List',
                    filters: {
                        'from_date': ['<=', frm.doc.from_date],
                        'to_date': ['>=', frm.doc.to_date]
                    },
                    fields: ['name', 'from_date', 'to_date'],
                    order_by: "creation desc",
                    limit_page_length: 1
                },
                callback: function (response) {
                    let holiday_list = response.message[0].name;
                    frm.call({
                        method: 'nxpo_hrms.custom.holiday.get_holiday_by_parent',
                        args: {
                            parent: holiday_list
                        },
                        callback: function (res) {
                            var holiday_all = res.message
                            if (holiday_all.length > 0) {
                                // Convert arrays to sets for efficient comparison
                                const available_dates_set = new Set(available_dates);
                                const holiday_all_set = new Set(holiday_all);
                                // Find intersection
                                const matching_dates = Array.from(available_dates_set).filter(date => holiday_all_set.has(date));
                                // Count matching dates
                                const matching_count = matching_dates.length;
                                var total_leave_days = days - matching_count
                                frm.set_value("total_leave_days", total_leave_days);
                                frm.trigger("get_leave_balance");
                            } else {
                                frm.set_value("total_leave_days", days);
                                frm.trigger("get_leave_balance");
                            }
                        }
                    });
                }
            });
        }
    },

    from_date: function (frm) {
        frm.events.validate_from_to_date(frm, "from_date");
        frm.trigger("calculate_total_days");
    },

    to_date: function (frm) {
        frm.events.validate_from_to_date(frm, "from_date");
        frm.trigger("calculate_total_days");

    }

});
