import frappe


def after_migrate():
	create_root_department_history()

def create_root_department_history():
	f = frappe.new_doc("Department History")
	f.department_name = "All Departments"
	f.insert(ignore_if_duplicate=True, ignore_mandatory=True)
