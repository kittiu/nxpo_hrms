import datetime
import frappe

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
        
    