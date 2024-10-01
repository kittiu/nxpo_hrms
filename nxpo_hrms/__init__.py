__version__ = "0.0.1"

# Monkey patching
# ------------------
# 1. Get Employee on Payroll Entry
import hrms.payroll.doctype.payroll_entry.payroll_entry as pe
from nxpo_hrms.custom.payroll_entry import get_filtered_employees
pe.get_filtered_employees = get_filtered_employees

# 2. Remove App Permission
import hrms.hr.utils as x
import erpnext as y
from nxpo_hrms.custom.permission import remove_app_permission
x.check_app_permission = remove_app_permission
y.check_app_permission = remove_app_permission
