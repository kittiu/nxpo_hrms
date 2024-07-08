# License: GNU General Public License v3. See license.txt
import frappe
from hrms.hr.doctype.leave_policy_assignment.leave_policy_assignment import LeavePolicyAssignment


class LeavePolicyAssignmentNXPO(LeavePolicyAssignment):

    def validate(self):
        if self.custom_addition_policy_assignment:
            self.set_dates()
            self.warn_about_carry_forwarding()
        else:
            super().validate()
