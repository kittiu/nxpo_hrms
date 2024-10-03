# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe import _



class SalaryCertificate(Document):
	def validate(self):
		if not self.employee:
			frappe.throw("กรุณาเลือกพนักงาน.")
	
		if not self.from_date:
			frappe.throw("กรุณาเลือก From Date.")
                          
		from_date = getdate(self.from_date)
		
		salary_structure_assignment = frappe.db.get_value(
            "Salary Structure Assignment",
            {
                "employee": self.employee,
                "from_date": ("<=", from_date)
            },
            ["name", "salary_structure", "base"],  
            as_dict=True
        )
		if not salary_structure_assignment:
			frappe.throw("ไม่พบ Salary Structure Assignment ที่ตรงกับ From Date ที่เลือก.")
			
		self.salary_structure_assignment = salary_structure_assignment.get("name")
		self.salary_structure = salary_structure_assignment.get("salary_structure")
		self.base_salary = salary_structure_assignment.get("base")
