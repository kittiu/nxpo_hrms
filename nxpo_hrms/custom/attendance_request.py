# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from hrms.hr.doctype.attendance_request.attendance_request import AttendanceRequest


class AttendanceRequestNXPO(AttendanceRequest):

	def create_or_update_attendance(self, date: str):
		super().create_or_update_attendance(date)
		# If work from home
		attendance_name = self.get_attendance_record(date)
		if attendance_name:
			doc = frappe.get_doc("Attendance", attendance_name)
			if doc.status == "Work From Home":
				doc.db_set({
					"status": "Present",
					"custom_work_from_anywhere": 1
				})
			elif doc.status in ("Absent", "On Leave"):
				doc.db_set({
					"custom_work_from_anywhere": 0
				})
