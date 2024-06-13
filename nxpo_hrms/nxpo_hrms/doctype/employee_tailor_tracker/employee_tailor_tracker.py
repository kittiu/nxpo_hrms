# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	add_years,
	getdate,
)


class EmployeeTailorTracker(Document):
    
	def on_insert(self):
		self.compute_round_balance()
    
	def on_update(self):
		self.compute_round_balance()

	def compute_round_balance(self):
		# Default
		balance = self.amount_per_round
		# Find if the tailor date is in existing round
		records = frappe.get_all(
			self.doctype,
			filters={
				"name": ("!=", self.name),
				"employee": self.employee,
				"start_date": ("<=", self.tailor_date),
				"end_date": (">=", self.tailor_date),
			},
			fields=["*"],
			order_by="tailor_date, name asc"
		)
		# Found the records for the same round, recompute all
		if records:
			old_rec = list(filter(lambda x: x["round"], records))[0]
			for doc in records + [self]: # Recompute all records on this round
				balance -= doc.tailor_amount or 0
				self.update_round_balance(doc.name, old_rec.round, old_rec.start_date, old_rec.end_date, balance)
			self.reload()
			return
		# No existing round, find new round
		round, start_date, end_date = self.get_new_round()
		balance -= self.tailor_amount
		self.update_round_balance(self.name, round, start_date, end_date, balance)
		self.reload()
	
	def update_round_balance(self, doc_name, round, start_date, end_date, balance):
		if not self.allow_over_budget and balance < 0:
			frappe.throw(
				_("Tailor amount is {0} over budget")
				.format(frappe.format(abs(balance), "Currency"))
			)
		print("---------------", doc_name, balance)
		frappe.db.set_value(self.doctype, doc_name, "round", round)
		frappe.db.set_value(self.doctype, doc_name, "start_date", start_date)
		frappe.db.set_value(self.doctype, doc_name, "end_date", end_date)
		frappe.db.set_value(self.doctype, doc_name, 'balance', balance)

	def get_new_round(self):
		# Possible new round can be,
		# 1. The tailor date
		# 2. Date after the last round
		years = self.years_per_round
		round = 1
		start_date = self.tailor_date
		prev_round = self.get_prev_round()
		if prev_round:
			round = prev_round.round + 1
			start_date = add_days(prev_round.end_date, 1)
		end_date = add_days(add_years(start_date, years), -1)
		while getdate(self.tailor_date) > getdate(end_date):
			start_date = add_years(start_date, years)
			end_date = add_days(add_years(start_date, years), -1)
			round += 1
		return (round, start_date, end_date)

	def get_prev_round(self):
		# Find the last round
		records = frappe.get_all(
			self.doctype,
			filters={
				"name": ("!=", self.name),
				"employee": self.employee,
				"end_date": ("<", self.tailor_date),
			},
			fields=["*"],
			order_by="end_date, name desc",
			limit=1
		)
		return records[0] if records else None

