# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, flt, getdate, month_diff


def get_period_factor(
	employee,
	start_date,
	end_date,
	payroll_frequency,
	payroll_period,
	depends_on_payment_days=0,
	joining_date=None,
	relieving_date=None,
):
	# TODO if both deduct checked update the factor to make tax consistent
	period_start, period_end = payroll_period.start_date, payroll_period.end_date

	if not joining_date and not relieving_date:
		joining_date, relieving_date = frappe.get_cached_value(
			"Employee", employee, ["date_of_joining", "relieving_date"]
		)

	if getdate(joining_date) > getdate(period_start):
		period_start = joining_date

	if relieving_date and getdate(relieving_date) < getdate(period_end):
		period_end = relieving_date
		# Patch by kittiu
		# if month_diff(period_end, start_date) > 1:
		# 	start_date = add_months(start_date, -(month_diff(period_end, start_date) + 1))

	total_sub_periods, remaining_sub_periods = 0.0, 0.0

	if payroll_frequency == "Monthly" and not depends_on_payment_days:
		total_sub_periods = month_diff(payroll_period.end_date, payroll_period.start_date)
		remaining_sub_periods = month_diff(period_end, start_date)
	else:
		salary_days = date_diff(end_date, start_date) + 1

		days_in_payroll_period = date_diff(payroll_period.end_date, payroll_period.start_date) + 1
		total_sub_periods = flt(days_in_payroll_period) / flt(salary_days)

		remaining_days_in_payroll_period = date_diff(period_end, start_date) + 1
		remaining_sub_periods = flt(remaining_days_in_payroll_period) / flt(salary_days)

	return total_sub_periods, remaining_sub_periods
