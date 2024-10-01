# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class OrgStructure(Document):

	def validate(self):
		self._check_type()
		self._check_structure()
	
	def on_submit(self):
		self._check_effective_date()
		self._apply_org_structure()

	def _check_type(self):
		departments = frappe.get_all(
			"Department",
			fields=["name", "custom_type"],
			as_list=1,
		)
		dept_dict = dict(departments)
		for idx, i in enumerate(self.items):
			d = list(filter(lambda x: x, [
				i.level_1,
				i.level_2,
				i.level_3,
				i.level_4
			]))
			if len(d) > 1:
				frappe.throw(_("Line# {} has more than one selection").format(idx+1))
			if not d:
				frappe.throw(_("Line# {} has no selection").format(idx+1))
			if dept_dict[d[0]] != i.type:
				frappe.throw(_("Line# {}, '{}' use invalid type '{}'").format(idx+1, d[0], i.type))

	def _check_structure(self):
		# Test that, the sturcture
		# - must start with level 1
		# - next line can't jump > 1 level
		prev_level = 1
		for idx, i in enumerate(self.items):
			if idx == 0 and not i.level_1:
				frappe.throw(_("Org Structure must start with Level 1"))
			_, level = get_dept_and_level(i)
			if (level - prev_level) > 1:
				frappe.throw(_("Org Structure is skipping level in Line# {}").format(idx+1))
			prev_level = level
	
	def _check_effective_date(self):
		if self.effective_date > today():
			frappe.throw(_("You cannot apply changes prior to effective date"))
	
	def _apply_org_structure(self):
		dept_names = [i.level_1 or i.level_2 or i.level_3 or i.level_4 for i in self.items]
		root_dept = frappe.db.get_value("Department", {"is_group": 1, "parent_department": None}, "name")
		dept_names.append(root_dept)
		# disable every department not in the list
		to_disable = frappe.get_all(
			"Department",
			filters={
				"company": self.company,
				"name": ["not in", dept_names]
			},
			pluck="name"
		)
		for dept in to_disable:
			frappe.set_value("Department", dept, "disabled", 1)
		# enable all departmet in list and change its parent structure
		prev_levels = {}
		for idx, i in enumerate(self.items):
			dept_name, level = get_dept_and_level(i)
			parent_dept = prev_levels[level-1] if level > 1 else root_dept
			frappe.db.set_value("Department", dept_name, {
				"is_group": 1,
				"disabled": 0,
				"parent_department": parent_dept,
				"custom_order": str(idx+1).zfill(3)
			})
			prev_levels[level] = dept_name


def get_dept_and_level(department):
	if department.level_1:
		return (department.level_1, 1)
	if department.level_2:
		return (department.level_2, 2)
	if department.level_3:
		return (department.level_3, 3)
	if department.level_4:
		return (department.level_4, 4)
	return (None, None)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_departments(doctype, txt, searchfield, start, page_len, filters):
	# Need to override because we also need result with disabled = True
	return frappe.db.sql(
		"""select name from tabDepartment
		where company = {} and custom_type = {}
		and {} like {} order by name limit {} offset {}""".format("%s", "%s", searchfield, "%s", "%s", "%s"),
		(filters["company"], filters["custom_type"], "%%%s%%" % txt, page_len, start),
		as_list=1,
	)
