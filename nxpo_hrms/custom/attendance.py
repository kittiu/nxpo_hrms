# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from hrms.hr.doctype.attendance.attendance import Attendance


class AttendanceNXPO(Attendance):

	def validate(self):
		super().validate()
		# Change work from home to present + work_from_anywhere
		if self.status == "Work From Home":
			self.status = "Present"
			self.custom_work_from_anywhere = 1
		elif self.status in ("Absent", "On Leave"):
			self.custom_work_from_anywhere = 0

