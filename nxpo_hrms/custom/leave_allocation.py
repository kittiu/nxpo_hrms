# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from frappe.query_builder import DocType
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json



@frappe.whitelist()
def get_unused_leave(data):
    LeaveLedgerEntry = DocType("Leave Ledger Entry")
    if isinstance(data, str):
        data = json.loads(data) 
    
    fd = data.get('from_date')
    td = data.get('to_date')

    # Convert the date strings to datetime objects if they are strings
    if isinstance(fd, str):
        fd_t = datetime.strptime(fd, '%Y-%m-%d') if fd else None
    else:
        fd_t = fd  # If already a datetime object, use it directly

    if isinstance(td, str):
        td_t = datetime.strptime(td, '%Y-%m-%d') if td else None
    else:
        td_t = td  # If already a datetime object, use it directly

    if fd_t:
        from_date_adjusted = fd_t - relativedelta(years=1)
        fd_ts = from_date_adjusted
        
    if td_t:
        to_date_adjusted = td_t - relativedelta(years=1)
        td_ts = to_date_adjusted
            
    # Build the query to sum the leaves
    query = (
        frappe.qb.from_(LeaveLedgerEntry)
        .where(
                (LeaveLedgerEntry.employee == data.get('employee')) & 
                (LeaveLedgerEntry.from_date >= fd_ts) & 
                (LeaveLedgerEntry.to_date <= td_ts)  & 
                (LeaveLedgerEntry.leave_type == data.get('leave_type'))
            )
        .select(Sum(LeaveLedgerEntry.leaves).as_("total_leaves"))
    )
        
    # Execute the query and get the result
    result = query.run()
        
    # Extract the total leaves from the result
    total_leaves = result[0][0] if result else 0

    return total_leaves


@frappe.whitelist()
def update_leave_allocation_unused_leave(names, action):
    # Ensure 'names' is a list
    if isinstance(names, str):
        import json
        names = json.loads(names) 

    is_add_unused_leave = 0

    if action == 'add_unused_leave':
        is_add_unused_leave = 1
    elif action == 'cancel_unused_leave':
        is_add_unused_leave = 0

    for name in names:
        total_unused_leave_value = '0'
        leave_allocation_data = frappe.db.get_value("Leave Allocation", name, "*", cache=True)
        
        if is_add_unused_leave == 1:
            total_unused_leave_value = get_unused_leave(leave_allocation_data)

        frappe.db.set_value('Leave Allocation', name, {
            'custom_total_unused_leave': total_unused_leave_value,
            'custom_is_add_unused_leave': is_add_unused_leave
        })
    frappe.db.commit() 

