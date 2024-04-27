# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta


class EmployeeInternalProbation(Document):

	def validate(self):
		# Update end of probation date
		self.date_end_probation = (
			getdate(self.date_start_probation) +
			relativedelta(days=self.probation_days)
		)
	
	def before_submit(self):
		if self.status not in ["Pass", "Not Pass"]:
			frappe.throw(_(
				"To submit, status of probation should be 'Pass' or 'Not Pass'"
			))
