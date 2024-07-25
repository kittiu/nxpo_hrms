# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import (
	getdate,
	today,
)

class ScholarshipInformation(Document):
    @frappe.whitelist()
    def dateOfDuration(self):
        start_date = self.start_date
        end_date = self.end_date
        diff = relativedelta(getdate(self.end_date), getdate(self.start_date))
        custom_date = _("{0} Years {1} Months {2} Days").format(
            diff.years, diff.months, diff.days
        )
        return custom_date




