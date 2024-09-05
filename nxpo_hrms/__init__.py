__version__ = "0.0.1"

# Monkey patching
# ------------------
# 1. Get Employee on Payroll Entry
import hrms.payroll.doctype.payroll_entry.payroll_entry as pe
from nxpo_hrms.custom.payroll_entry import get_filtered_employees
pe.get_filtered_employees = get_filtered_employees

