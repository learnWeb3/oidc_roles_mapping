app_name = "oidc_roles_mapping"
app_title = "Oidc Roles Mapping"
app_publisher = "Antoine LE GUILLOU"
app_description = "OIDC role mapping capabilities"
app_email = "antoinehadrienleguillou@outlook.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/oidc_roles_mapping/css/oidc_roles_mapping.css"
# app_include_js = "/assets/oidc_roles_mapping/js/oidc_roles_mapping.js"

# include js, css files in header of web template
# web_include_css = "/assets/oidc_roles_mapping/css/oidc_roles_mapping.css"
# web_include_js = "/assets/oidc_roles_mapping/js/oidc_roles_mapping.js"

# include custom callback.py

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "oidc_roles_mapping/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "oidc_roles_mapping/public/icons.svg"

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
# 	"methods": "oidc_roles_mapping.utils.jinja_methods",
# 	"filters": "oidc_roles_mapping.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "oidc_roles_mapping.install.before_install"
# after_install = "oidc_roles_mapping.install.after_install"
after_install = "oidc_roles_mapping.setup.install.after_install"
before_uninstall = "oidc_roles_mapping.setup.uninstall.before_uninstall"

# Uninstallation
# ------------

# before_uninstall = "oidc_roles_mapping.uninstall.before_uninstall"
# after_uninstall = "oidc_roles_mapping.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "oidc_roles_mapping.utils.before_app_install"
# after_app_install = "oidc_roles_mapping.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "oidc_roles_mapping.utils.before_app_uninstall"
# after_app_uninstall = "oidc_roles_mapping.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "oidc_roles_mapping.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"oidc_roles_mapping.tasks.all"
# 	],
# 	"daily": [
# 		"oidc_roles_mapping.tasks.daily"
# 	],
# 	"hourly": [
# 		"oidc_roles_mapping.tasks.hourly"
# 	],
# 	"weekly": [
# 		"oidc_roles_mapping.tasks.weekly"
# 	],
# 	"monthly": [
# 		"oidc_roles_mapping.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "oidc_roles_mapping.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.integrations.oauth2_logins.custom": "oidc_roles_mapping.overrides.oauth2_logins.custom"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "oidc_roles_mapping.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["oidc_roles_mapping.custom_auth.verify_jwt_token"]
# after_request = ["oidc_roles_mapping.utils.after_request"]

# Job Events
# ----------
# before_job = ["oidc_roles_mapping.utils.before_job"]
# after_job = ["oidc_roles_mapping.utils.after_job"]

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

auth_hooks = [
	"oidc_roles_mapping.overrides.auth.validate_custom_jwt"
]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

required_apps = ["frappe", "erpnext"]

