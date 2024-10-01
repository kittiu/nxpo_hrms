__version__ = "0.0.1"

# Monkey patching
# ------------------
# 1. Get Employee on Payroll Entry
import hrms.payroll.doctype.payroll_entry.payroll_entry as pe
from nxpo_hrms.custom.payroll_entry import get_filtered_employees
pe.get_filtered_employees = get_filtered_employees

# 2. Remove App Permission
import hrms.hooks as a
import erpnext.hooks as b
import wiki.hooks as c
import drive.hooks as d
a.add_to_apps_screen = []
b.add_to_apps_screen = []
c.add_to_apps_screen = []
d.add_to_apps_screen = []
