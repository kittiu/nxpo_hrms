import datetime
import frappe
from num2words import num2words


def amount_in_bahttext(amount):
	return num2words(amount, to="currency", lang="th")


def full_thai_date(date_str):
	if not date_str:
		return ""
	date = datetime.datetime.strptime(str(date_str), "%Y-%m-%d")
	month_name = "x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม".split()[
		date.month
	]
	thai_year = date.year + 543
	return "%d %s %d" % (date.day, month_name, thai_year)  # 30 ตุลาคม 2560


def thai_date(date_str):
    # return Thai date which has year = date.year + 543
    if not date_str:
        return ""
    date = datetime.datetime.strptime(str(date_str), "%Y-%m-%d")
    thai_year = date.year + 543
    return "%d/%d/%d" % (date.day, date.month, thai_year)  # 30/10/2560


def get_employee_name_by_user(user):
    if not user:
        return ""
    emp_id = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not emp_id:
        return ""
    employee = frappe.get_cached_doc("Employee", emp_id)
    return employee.employee_name
