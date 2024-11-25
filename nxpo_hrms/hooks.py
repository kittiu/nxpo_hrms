app_name = "nxpo_hrms"
app_title = "NXPO HRMS"
app_publisher = "Ecosoft"
app_description = "NXPO HRMS"
app_email = "kittiu@ecosoft.co.th"
app_license = "mit"
required_apps = ["thai_leave"]

fixtures = [
    {
        "doctype": "Workflow State",
        "filters": [
            [
                "name",
                "in",
                (
                    "Pending Approval",
                    "Cancelled",
                )
            ]
        ]
    },
    {
        "doctype": "Workflow",
        "filters": [
            [
                "name",
                "in",
                (
                    "NXPO Leave Application",
                    "NXPO Offsite Work Request",
                )
            ]
        ]
    },
    # {
    #     "doctype": "Recruitment Type",
    #     "filters": [
    #         [
    #             "name",
    #             "in",
    #             (
    #                 "สรรหา",
    #                 "คัดเลือก",
    #                 "ยืมตัว",
    #                 "นักเรียนทุน",
    #                 "แต่งตั้ง",
    #                 "โอนย้าย",
    #                 "ต่อสัญญา",
    #             )
    #         ]
    #     ]
    # },
    # {
    #     "doctype": "Employee Agreement Type",
    #     "filters": [
    #         [
    #             "name",
    #             "in",
    #             (
    #                 "สัญญาจ้างพนักงาน",
    #                 "สัญญาจ้างพนักงานโครงการ",
    #                 "สัญญาจ้างตามวาระ",
    #                 "สัญญาจ้างผู้ทรงคุณวุฒิ",
    #                 "สัญญาระหว่างหน่วยงาน (ยืมตัว)",
    #                 "ผู้ขับเคลื่อนพันธกิจเฉพาะเรื่อง",
    #                 "ภาคีวิจัยนโยบาย",
    #             )
    #         ]
    #     ]
    # },
    # {
    #     "doctype": "PVD Type",
    #     "filters": [
    #         [
    #             "name",
    #             "in",
    #             (
    #                 "กองทุนสำรองเลี้ยงชีพ (ผสมหุ้นไม่เกิน 25%)",
    #                 "กองทุนสำรองเลี้ยงชีพ (ผสมหุ้นไม่เกิน 10%)",
    #                 "กองทุนสำรองเลี้ยงชีพ (ตราสารหนี้)",
    #                 "กองทุนสำรองเลี้ยงชีพ (DIY)",
    #             )
    #         ]
    #     ]
    # },
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                (
                    "PND1a NXPO",
                )
            ]
        ]
    },
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Company-custom_policy",
                    "Company-custom_owr_days_per_week",
                    "Offsite Work Request-workflow_state",
                )
            ]
        ]
    },
    {
        "doctype": "Role",
        "filters": [
            ["name", "in", ["Payroll User", "User Admin"]]
        ]
    },
    {
        "doctype": "Custom DocPerm",
        "filters": [
            ["name", "in", [
                "umrsa4svvl",
                "umrs35nh8j",
                "umrsmga4pc",
                "suhbscgpa6",
                "stusri3f4n",
            ]]
        ]
    },
]

# fixtures = [
#     {
#         "doctype": "Custom Field",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 (
#                     "Employee-custom_probation_days",
#                     "Employee-custom_date_pass_probation",
#                     "Employee-custom_summary",
#                     "Employee-custom_summary_html",
#                     "Employee-custom_property_history_html",
#                     "Employee-custom_experience_ytd",
#                 )
#             ]
#         ]
#     },
#     {
#         "doctype": "Property Setter",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 (
#                     "Employee-internal_work_history-hidden",
#                     "Employee-internal_work_history-print_hide",
#                     "Employee-internal_work_history-report_hide",
#                     "Employee-history_in_company-collapsible",
#                     "Employee-previous_work_experience-collapsible_depends_on",
#                     "Employee-educational_qualification-collapsible_depends_on",
#                 )
#             ]
#         ]
#     }
# ]



# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nxpo_hrms/css/nxpo_hrms.css"
app_include_js = "nxpo_hrms.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/nxpo_hrms/css/nxpo_hrms.css"
# web_include_js = "/assets/nxpo_hrms/js/nxpo_hrms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nxpo_hrms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Employee": "public/js/employee.js",
    "Salary Structure Assignment": "public/js/salary_structure_assignment.js",
    "Leave Allocation": "public/js/leave_allocation.js",
    "Additional Salary": "public/js/additional_salary.js",
    "Attendance": "public/js/attendance.js",
    "Employee Attendance Tool": "public/js/employee_attendance_tool.js",
    "Leave Application": "public/js/leave_application.js",
}
doctype_tree_js = {
    "Department" : "public/js/department_tree.js"
}

doctype_list_js = {
    "Leave Allocation": "public/js/leave_allocation.js",
}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "nxpo_hrms/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": "nxpo_hrms.custom.payroll_entry.sum_amount_ss_component",
	# "filters": "nxpo_hrms.utils.jinja_filters"
}

# Installation
# ------------

# before_install = "nxpo_hrms.install.before_install"
# after_install = "nxpo_hrms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nxpo_hrms.uninstall.before_uninstall"
# after_uninstall = "nxpo_hrms.uninstall.after_uninstall"

after_migrate = ["nxpo_hrms.custom.salary_slip.set_print_format_as_custom"]

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "nxpo_hrms.utils.before_app_install"
# after_app_install = "nxpo_hrms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "nxpo_hrms.utils.before_app_uninstall"
# after_app_uninstall = "nxpo_hrms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nxpo_hrms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Salary Slip": "nxpo_hrms.custom.salary_slip.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee": "nxpo_hrms.custom.employee.EmployeeNXPO",
    "Salary Slip": "nxpo_hrms.custom.salary_slip.SalarySlipNXPO",
	"Salary Structure Assignment": "nxpo_hrms.custom.salary_structure_assignment.SalaryStructureAssignmentNXPO",
    "Leave Policy Assignment": "nxpo_hrms.custom.leave_policy_assignment.LeavePolicyAssignmentNXPO",
    "Attendance Request": "nxpo_hrms.custom.attendance_request.AttendanceRequestNXPO",
    "Attendance": "nxpo_hrms.custom.attendance.AttendanceNXPO",
    "Leave Application": "nxpo_hrms.custom.leave_application.LeaveApplicationNXPO",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Employee": {
        "validate": [
            "nxpo_hrms.custom.employee.update_employee_data",
            "nxpo_hrms.custom.employee.update_current_address",
            "nxpo_hrms.custom.employee.update_permanent_address",
        ]
    },
    "Payroll Entry": {
        "validate": [
            "nxpo_hrms.custom.payroll_entry.validate_posting_date",
        ]
    },
    "Salary Slip": {
        "validate": [
            "nxpo_hrms.custom.payroll_entry.validate_posting_date",
            "nxpo_hrms.custom.salary_slip.validate_no_salary",
        ]
    },
    "User": {
        "validate": [
            "nxpo_hrms.custom.user.create_user_own_role",
            "nxpo_hrms.custom.user.validate_update_role_profile",
        ]
    },
    "Leave Application": {
        "validate": "nxpo_hrms.custom.leave_application.compute_approver",
        "on_update": "nxpo_hrms.custom.leave_application.share_to_approver",
    },
    "Offsite Work Request": {  # Reusing exact same logic for approver as Leave Application
        "validate": "nxpo_hrms.custom.leave_application.compute_approver",
        "on_update": "nxpo_hrms.custom.leave_application.share_to_approver",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly": [
        "nxpo_hrms.nxpo_hrms.doctype.offsite_work_request.offsite_work_request.auto_create_attendance_requests",
        "nxpo_hrms.nxpo_hrms.doctype.employee_special_assignment.employee_special_assignment.job_update_active",
        "nxpo_hrms.nxpo_hrms.doctype.tigersoft_connector.tigersoft_connector.sync_employee_checkin",
    ],
    "daily": [
        "nxpo_hrms.nxpo_hrms.doctype.tigersoft_connector.tigersoft_connector.sync_offsite_work_request",
        "nxpo_hrms.nxpo_hrms.doctype.tigersoft_connector.tigersoft_connector.sync_leave_application",
    ],
}

# Testing
# -------

# before_tests = "nxpo_hrms.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.core.doctype.user.user.get_all_roles": "nxpo_hrms.custom.user.get_all_roles",
    "hrms.hr.doctype.employee_attendance_tool.employee_attendance_tool.get_employees": "nxpo_hrms.custom.employee_attendance_tool.get_employees",
    "erpnext.setup.doctype.employee.employee.create_user": "nxpo_hrms.custom.employee.create_user",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nxpo_hrms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["nxpo_hrms.utils.before_request"]
# after_request = ["nxpo_hrms.utils.after_request"]

# Job Events
# ----------
# before_job = ["nxpo_hrms.utils.before_job"]
# after_job = ["nxpo_hrms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nxpo_hrms.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

company_data_to_be_ignored = [
    "Department",
    "Leave Period",
    "Payroll Period",
    "Salary Structure",
    # "Leave Allocation",
    # "Leave Policy Assignment",
    # "Employee Tax Exemption Declaration",
    # "Additional Salary",
    # "Salary Structure Assignment",
    # "Payroll Entry",
    # "Salary Slip",
    # "Org Structure",
    # "Employee Transition",  
]