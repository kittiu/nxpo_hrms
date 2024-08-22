# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

@frappe.whitelist()
def get_holiday_by_parent(parent):
    holiday_list = frappe.db.get_all('Holiday', 
        filters={
            'parent': parent
        },
        pluck="holiday_date"
        )
    return holiday_list