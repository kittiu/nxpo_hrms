# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from frappe.query_builder import DocType
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta


class LeaveAllocationNXPO(Document):

    @frappe.whitelist(allow_guest=True)
    def get_leave_ledger(self, data):

        LeaveLedgerEntry = DocType("Leave Ledger Entry")

        fd = data.get('from_date')
        td = data.get('to_date')

        # Convert the date strings to datetime objects
        fd_t = datetime.strptime(fd, '%Y-%m-%d') if fd else None
        td_t = datetime.strptime(td, '%Y-%m-%d') if td else None

        if fd_t:
            from_date_adjusted = fd_t - relativedelta(years=1)
            fd_ts = from_date_adjusted
        
        if td_t:
            to_date_adjusted = td_t - relativedelta(years=1)
            td_ts = to_date_adjusted
            
        # Build the query to sum the amount
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
        
        # Extract the total amount from the result
        total_leaves = result[0][0] if result else 0

        return total_leaves


