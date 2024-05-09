app_name = "nxpo_hrms"
app_title = "NXPO HRMS"
app_publisher = "Ecosoft"
app_description = "NXPO HRMS"
app_email = "kittiu@ecosoft.co.th"
app_license = "mit"
# required_apps = []

fixtures = [
    {
        "doctype": "Recruitment Type",
        "filters": [
            [
                "name",
                "in",
                (
                    "สรรหา",
                    "คัดเลือก",
                    "ยืมตัว",
                    "นักเรียนทุน",
                    "แต่งตั้ง",
                    "โอนย้าย",
                    "ต่อสัญญา",
                )
            ]
        ]
    },
    {
        "doctype": "Employee Agreement Type",
        "filters": [
            [
                "name",
                "in",
                (
                    "สัญญาจ้างพนักงาน",
                    "สัญญาจ้างพนักงานโครงการ",
                    "สัญญาจ้างตามวาระ",
                    "สัญญาจ้างผู้ทรงคุณวุฒิ",
                    "สัญญาระหว่างหน่วยงาน (ยืมตัว)",
                    "ผู้ขับเคลื่อนพันธกิจเฉพาะเรื่อง",
                    "ภาคีวิจัยนโยบาย",
                )
            ]
        ]
    },
    {
        "doctype": "PVD Type",
        "filters": [
            [
                "name",
                "in",
                (
                    "กองทุนสำรองเลี้ยงชีพ (ผสมหุ้นไม่เกิน 25%)",
                    "กองทุนสำรองเลี้ยงชีพ (ผสมหุ้นไม่เกิน 10%)",
                    "กองทุนสำรองเลี้ยงชีพ (ตราสารหนี้)",
                    "กองทุนสำรองเลี้ยงชีพ (DIY)",
                )
            ]
        ]
    },
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
    }
]

# fixtures = [
#     {
#         "doctype": "Custom Field",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 (
#                     "Employee Transfer-custom_notify_users_by_email",
#                     "Employee Transfer-custom_transfer_activities",
#                     "Employee Transfer-custom_employee_transfer_template",
#                     "Employee Transfer-custom_section_activities",
#                     "Employee Transfer-custom_project",
#                     "Employee Transfer-custom_transition_status",
#                     "Employee Transfer-custom_auto_submit",
#                     "Employee Promotion-custom_employee_promotion_template",
#                     "Employee Promotion-custom_project",
#                     "Employee Promotion-custom_transition_status",
#                     "Employee Promotion-custom_notify_users_by_email",
#                     "Employee Promotion-custom_section_activities",
#                     "Employee Promotion-custom_promotion_activities",
#                     "Employee Promotion-custom_auto_submit",
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
# app_include_js = "/assets/nxpo_hrms/js/nxpo_hrms.js"

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
    "Employee Promotion": "public/js/employee_promotion.js",
    "Employee Transfer": "public/js/employee_transfer.js",
    "Employee": "public/js/employee.js",
}
doctype_list_js = {
    "Employee Promotion": "public/js/employee_promotion_list.js",
    "Employee Transfer": "public/js/employee_transfer_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
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
# jinja = {
# 	"methods": "nxpo_hrms.utils.jinja_methods",
# 	"filters": "nxpo_hrms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "nxpo_hrms.install.before_install"
# after_install = "nxpo_hrms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nxpo_hrms.uninstall.before_uninstall"
# after_uninstall = "nxpo_hrms.uninstall.after_uninstall"

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
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee": "nxpo_hrms.custom.employee.EmployeeNXPO"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Employee Promotion": {
        "validate": "nxpo_hrms.custom.employee_transition.remove_task_from_activities",
        "on_submit": "nxpo_hrms.custom.employee_transition.create_project",
        "on_cancel": "nxpo_hrms.custom.employee_transition.delete_project_task",
        "on_update_after_submit": "nxpo_hrms.custom.employee_transition.create_task_and_notify_user",
    },
    "Employee Transfer": {
        "validate": [
            "nxpo_hrms.custom.employee_transition.remove_task_from_activities",
            "nxpo_hrms.custom.employee_transition.check_employee_internal_probation",
        ],
        "on_submit": "nxpo_hrms.custom.employee_transition.create_project",
        "on_cancel": "nxpo_hrms.custom.employee_transition.delete_project_task",
        "on_update_after_submit": "nxpo_hrms.custom.employee_transition.create_task_and_notify_user",
    },
    "Project": {
        "validate": "nxpo_hrms.custom.employee_transition.update_employee_transition_status"
    },
    "Task": {"on_update": "nxpo_hrms.custom.employee_transition.update_task"},
    "Employee": {
        "validate": [
            "nxpo_hrms.custom.employee.update_employee_data",
            "nxpo_hrms.custom.employee.update_current_address",
        ]
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    # "all": [
    #     "nxpo_hrms.custom.employee_transition.auto_submit"
    # ],
    # "daily": [
    #     "nxpo_hrms.custom.employee.update_all_employee_data"
    # ],
    "hourly": [
        "nxpo_hrms.custom.employee_transition.auto_submit"
    ],
    # "weekly": [
    # 	"nxpo_hrms.tasks.weekly"
    # ],
    # "monthly": [
    # 	"nxpo_hrms.tasks.monthly"
    # ],
}

# Testing
# -------

# before_tests = "nxpo_hrms.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.setup.doctype.department.department.get_children": "nxpo_hrms.custom.department.get_children"
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

