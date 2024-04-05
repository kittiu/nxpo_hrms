# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from dateutil.relativedelta import relativedelta
from frappe.utils import getdate


def update_employee_data(doc, method=None):
    doc.custom_date_pass_probation = (
        getdate(doc.date_of_joining) +
        relativedelta(days=doc.custom_probation_days)
    )
