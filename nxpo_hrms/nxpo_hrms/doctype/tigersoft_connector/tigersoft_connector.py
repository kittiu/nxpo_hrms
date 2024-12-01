# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import math
import ast
try:
	import pymssql
except:
	pass


class TigersoftConnector(Document):

	def _cr(self):
        # Setting Database Parameters
		server = str(self.ip_address)
		user = str(self.user)
		password = str(self.password)
		port = str(self.port)
		database = str(self.db_name)
		conn = pymssql.connect(server, user, password, database, port=port)
		return conn.cursor()


def sync_employee_checkin():
	"""
	1. Get latest checkin date for all employee
	2. Loop through each employee and get checkin from Tiger that is after latest checking date
	3. Insert new checkin to frappe	
	"""
	frappe.flags.sync_tigersoft = True

	settings = frappe.get_single("Tigersoft Connector")
	if not settings.sync_employee_checkin:
		return
	mssql = settings._cr()
	
	# Get latest checkin date for all employee
	emp_last_checkins = frappe.db.sql("""
		select e.employee, max(c.time)  from `tabEmployee` e
		left outer join `tabEmployee Checkin` c on c.employee = e.name
		group by e.employee
	""")
	
	# Loop through each employee and create checkin transactions
	for employee, last_checkin in emp_last_checkins:
		sql = """
			select distinct employee_code, date_in_out
			from frappe_vwTigerTimeInOut
			where 
		"""
		if last_checkin:
			mssql.execute(sql + """
				employee_code = %s and date_in_out > %s order by date_in_out
			""", (employee, last_checkin))
		else:
			mssql.execute(sql +"""
				 employee_code = %s order by date_in_out
			""", (employee,))
		rows = mssql.fetchall()
		if not rows:
			continue
		for row in rows:
			checkin = frappe.new_doc("Employee Checkin")
			checkin.employee = row[0]
			checkin.log_type = "IN"
			checkin.time = row[1]
			checkin.insert()
		# Commit when finish 1 employee
		frappe.db.commit()
		

def sync_offsite_work_request():
	frappe.flags.sync_tigersoft = True

	settings = frappe.get_single("Tigersoft Connector")
	if not settings.sync_offsite_work_request:
		return
	mssql = settings._cr()
	
	# Get latest approved date OWR for all employee, so to sync only new ones
	emp_last_offsite_works = frappe.db.sql("""
		select e.employee, max(r.tigersoft_approve_date)  from `tabEmployee` e
		left outer join `tabOffsite Work Request` r on r.employee = e.name
		group by e.employee
	""")

	doc = frappe.get_single("Tigersoft Connector")
	map_leave = ast.literal_eval(doc.offsite_work_mapping or "{}")
	leave_names = tuple(map_leave.keys())
	if not leave_names:
		return
	
	# Loop through each employee and create owr transactions
	for employee, last_approve in emp_last_offsite_works:
		sql = """
			select 
				employee_code,
				leave_name,
				leave_memo,
				leave_type_name,
				leave_date_start,
				leave_date_end,
				approve_date
			from frappe_vwTigerLeaveForm
			where approve = 'A' and status_delete = 0
			and leave_name in %s
		""" % str(leave_names)
		if last_approve:
			mssql.execute(sql + """
				and employee_code = %s and approve_date > %s
				order by approve_date
			""", (employee, last_approve))
		else:
			mssql.execute(sql + """
				and employee_code = %s
				order by approve_date
			""", (employee,))
		rows = mssql.fetchall()
		if not rows:
			continue

		for (
			employee_code,
			leave_name,
			leave_memo,
			leave_type_name,
			leave_date_start,
			leave_date_end,
			approve_date
		) in rows:
			owr = frappe.new_doc("Offsite Work Request")
			owr.employee = employee_code
			owr.type = map_leave[leave_name][0]
			owr.event = map_leave[leave_name][1]
			owr.note = leave_memo
			owr.tigersoft_approve_date = approve_date
			half_day = 1 if (
				"ลาครึ่งวัน" in leave_type_name or
				"ลาช่วงเวลา" in leave_type_name
			) else 0
			owr.append("plan_dates", {
				"from_date": leave_date_start,
				"to_date": leave_date_end,
				"half_day": half_day,
				"half_day_date": leave_date_start if half_day else ""
			})
			owr.insert()
			owr.submit()  # Submit by Admin
			# Commit when finish 1 employee
			frappe.db.commit()
		

def sync_leave_application():
	settings = frappe.get_single("Tigersoft Connector")
	if not settings.sync_leave_application:
		return
	mssql = settings._cr()
	
	# Get latest approved OWR for all employee
	emp_last_leave_apps = frappe.db.sql("""
		select e.employee, max(l.custom_tigersoft_approve_date)  from `tabEmployee` e
		left outer join `tabLeave Application` l on l.employee = e.name
		group by e.employee
	""")

	doc = frappe.get_single("Tigersoft Connector")
	map_leave = ast.literal_eval(doc.leave_type_mapping or "{}")
	leave_names = tuple(map_leave.keys())
	if not leave_names:
		return

	# Loop through each employee and create owr transactions
	for employee, last_approve in emp_last_leave_apps:
		sql = """
			select
				employee_code,
				leave_name, leave_memo, leave_type_name,
				leave_date_start, leave_date_end,
				case when leave_type_name like 'ลาช่วง%%'
              		then DATEPART(HOUR, CONVERT(TIME, leave_time_total))
					+ DATEPART(MINUTE, CONVERT(TIME, leave_time_total)) / 60
            	else
              		0
				end leave_time_total,
				approve_date
			from frappe_vwTigerLeaveForm
			where approve = 'A' and status_delete = 0 
			and leave_name in %s
		""" % str(leave_names)
		if last_approve:
			mssql.execute(sql + """
				and employee_code = %s and approve_date > %s
				order by approve_date
			""", (employee, last_approve))
		else:
			mssql.execute(sql + """
				and employee_code = %s
				order by approve_date
			""", (employee,))
		rows = mssql.fetchall()
		if not rows:
			continue

		for (
			employee_code,
			leave_name,
			leave_memo,
			leave_type_name,
			leave_date_start,
			leave_date_end,
			leave_time_total,
			approve_date
		) in rows:
			leave = frappe.new_doc("Leave Application")
			leave.employee = employee_code
			leave.leave_type = map_leave[leave_name]
			leave.description = leave_memo
			leave.custom_tigersoft_approve_date = approve_date
			leave.half_day = 1 if (
				"ลาครึ่งวัน" in leave_type_name or
				"ลาช่วงเวลา" in leave_type_name
			) else 0
			hours = math.ceil(leave_time_total)
			if hours > 0:
				leave.custom_hours = str(hours)
			leave.from_date = leave_date_start
			leave.to_date = leave_date_end
			leave.status = "Approved"
			# Set before save to skip validation
			frappe.flags.sync_tigersoft = True
			leave.save()  # make sure it is validated
			frappe.db.commit()
			# --
			try:  # Try to submit, but it is ok if failed.
				frappe.flags.sync_tigersoft = False  # To validate again
				leave.submit()
				frappe.db.commit()
			except:
				pass
