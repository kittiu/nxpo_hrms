# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe import share


class SalaryCertificate(Document):

	def validate(self):
		self.set_salary_info()

	def on_update(self):
		self.share_to_approver()

	def set_salary_info(self):
		ssa = frappe.get_all(
            "Salary Structure Assignment",
            {
                "employee": self.employee,
                "from_date": ("<=", self.date_of_certification),
				"docstatus": 1,
            },
            ["name", "base"],
			order_by="from_date desc",
			limit=1
        )

		if not ssa:
			frappe.throw(_("Salary Structure Assignment not found for Employee {0}").format(self.employee))

		self.salary_structure_assignment = ssa[0].name
		self.base_salary = ssa[0].base

	def share_to_approver(self):
		users = [x.user for x in share.get_users(self.doctype, self.name)]
		for user in users:
			if user != frappe.session.user:
				share.remove(self.doctype, self.name, user)
		if self.approver and self.approver != frappe.session.user:
			share.add_docshare(self.doctype, self.name, user=self.approver, read=1, submit=1, notify=1)
