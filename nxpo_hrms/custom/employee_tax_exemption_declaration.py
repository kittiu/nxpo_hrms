
from datetime import date
import frappe
from frappe import _, msgprint
from frappe.utils.background_jobs import enqueue
from frappe.model.document import Document

from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import EmployeeTaxExemptionDeclaration


class EmployeeTaxExemptionDeclarationNXPO(EmployeeTaxExemptionDeclaration):
    def email_employee_tax_exemption_declaration(self):
        receiver = frappe.db.get_value("Employee", self.employee, "prefered_email", cache=True)
        company = frappe.db.get_value("Employee", self.employee, "company", cache=True)
    
        payroll_settings = frappe.get_single("Payroll Settings")
        subject = f"Employee Tax Exemption Declaration"
        message = _("Please")

        # Fixed
        email_template_name = 'Employee Tax Exemption Declaration'

        if company:
            email_template_name = frappe.db.get_value("Company", company, "custom_email_template_for_employee_tax_exempt_declaration", cache=True)
            
        email_template = frappe.get_doc("Email Template", email_template_name)

        if payroll_settings:
            sender = payroll_settings.sender_email
        else:
            sender = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id", cache=True)

        if email_template:
            context = self.as_dict()

            custom_link = frappe.utils.get_url("/app/employee-tax-exemption-declaration/" + self.name)
            html_link =  f"""<a href='{custom_link}' target='blank'>Employee Tax Exemption Declaration</a>"""

            context['link'] = html_link
            subject = frappe.render_template(email_template.subject, context)
            message = frappe.render_template(email_template.response, context)

        if receiver:
            email_args = {
                "sender": sender,
                "recipients": [receiver],
                "message": message,
                "subject": subject,
                "reference_doctype": self.doctype,
                "reference_name": self.name,
            }
            if not frappe.flags.in_test:
                enqueue(method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args)
            else:
                frappe.sendmail(**email_args)
        else:
            msgprint(_("{0}: Employee email not found, hence email not sent").format(self.employee_name))


@frappe.whitelist()
def enqueue_email_employee_tax_exemption_declaration(names) -> None:
    """enqueue bulk emailing enqueue_email_employee_tax_exemption_declaration"""
    import json

    if isinstance(names, str):
        names = json.loads(names)
    
    frappe.enqueue("nxpo_hrms.custom.employee_tax_exemption_declaration.email_employee_tax_exemption_declarations", names=names)
    # email_employee_tax_exemption_declarations(names)
    frappe.msgprint(
        _("Employee Tax Exemption Declaration emails have been enqueued for sending. Check {0} for status.").format(
            f"""<a href='{frappe.utils.get_url_to_list("Email Queue")}' target='blank'>Email Queue</a>"""
        )
    )

def email_employee_tax_exemption_declarations(names) -> None:
    for name in names:
        employee_tax_exemption_declaration = frappe.get_doc("Employee Tax Exemption Declaration", name)
        employee_tax_exemption_declaration.email_employee_tax_exemption_declaration()
