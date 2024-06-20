# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
from frappe import _
from dateutil.relativedelta import relativedelta
from frappe.model.document import Document
from frappe.utils import (
	getdate,
	today,
)


class EmployeeFamilyMembers(Document):

    @property
    def age(self):
        diff = relativedelta(getdate(today()), getdate(self.date_of_birth))
        age = _("{0} Years").format(diff.years)
        return age