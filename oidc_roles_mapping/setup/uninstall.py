import frappe
import os.path
from oidc_roles_mapping.setup.yaml_parser  import parse


def before_uninstall():
    cleanup()


def cleanup_role(role={
    "name": "Invoice Manager",
    "rights": [
        {
            "doc_type": "Sales Invoice",
            "permissions": {"read": 1, "write": 1, "create": 1}
        }
    ]
}):
    try:
        role_permissions = frappe.get_list("Custom DocPerm", filters={"role": role['name'], })
        for role_permission in role_permissions:
            frappe.delete_doc("Custom DocPerm",   role_permission['name'])
            
        frappe.delete_doc("Role",   role['name'])
    except frappe.DoesNotExistError:
        print(f"Document { role['name']} does not exist.")

    except frappe.PermissionError:
        print(f"You do not have permission to delete document { role['name']}.")
        
    except Exception as e:
        print(f"Error deleting document {role['name']}: {e}")

def cleanup_role_profile(role_profile={
    "name": "webservice",
    "roles": ["Invoice Manager"]
}):
    try:
        frappe.delete_doc("Role Profile",   role_profile['name'])
    except frappe.DoesNotExistError:
        print(f"Document {role_profile['name']} does not exist.")

    except frappe.PermissionError:
        print(f"You do not have permission to delete document {role_profile['name']}.")

    except Exception as e:
        print(f"Error deleting document {role_profile['name']}: {e}")

def cleanup_social_login_key(social_login_key={
        "name":  "keycloak", # provider_name
        "enable": 1, # enable_social_login
        "social_login_provider": "Custom",
        "client_id": "andrew-erp",
        "client_secret": "",
        "base_url": "https://login.students-epitech.ovh/realms/andrew",
        "base64icon": "", # icon
        "allow_sign_up": 1, # sign_ups values Allow Deny
        "authorize_uri": "/protocol/openid-connect/auth", # authorize_uri
        "access_token_uri": "/protocol/openid-connect/token", # access_token_url
        "redirect_url": "http://localhost:8000/api/method/frappe.integrations.oauth2_logins.custom/keycloak",
        "api_endpoint": "https://login.students-epitech.ovh/realms/andrew/protocol/openid-connect/userinfo",
        "api_endpoint_args": "",
        "auth_url_data": "{\"response_type\": \"code\", \"scope\": \"openid profile email\"}",
        "user_claim": "email",  #  user_id_property
        "role_claim": "roles",
        "secret_key": "",
        "audience": "",
        "offline_validate": 0,
}):
    try:
        filters = {"social_login_key_name":  social_login_key['name']}
        # Use frappe.get_list to retrieve the list of documents
        social_login_extensions_to_delete = frappe.get_list( "Social Login Key Extension", filters=filters)
        
        for social_login_extension_to_delete in social_login_extensions_to_delete:
            frappe.delete_doc("Social Login Key Extension", social_login_extension_to_delete['name'])

        frappe.delete_doc("Social Login Key",   social_login_key['name'])
    except frappe.DoesNotExistError:
        print(f"Document {social_login_key['name']} does not exist.")

    except frappe.PermissionError:
        print(f"You do not have permission to delete document {social_login_key['name']}.")

    except Exception as e:
        print(f"Error deleting document {social_login_key['name']}: {e}")

def cleanup_role_profile_mapping(role_profile_mapping={
        "name": "superadmin claim to superadmin role profile",
        "role_profile": "superadmin",
        "role_claim_value": "superadmin",
        "client": "keycloak",
}):
    try:
        frappe.delete_doc("Role Profile Mapping",   role_profile_mapping['name'])
    except frappe.DoesNotExistError:
        print(f"Document {role_profile_mapping['name']} does not exist.")

    except frappe.PermissionError:
        print(f"You do not have permission to delete document {role_profile_mapping['name']}.")

    except Exception as e:
        print(f"Error deleting document {role_profile_mapping['name']}: {e}")
        
        
def cleanup_custom_doctype(doctype_name):
    try:
        frappe.delete_doc("DocType", doctype_name, ignore_permissions=True)

        print(f"Custom DocType {doctype_name} deleted successfully.")

    except frappe.DoesNotExistError:
        print(f"Custom DocType {doctype_name} does not exist.")

    except frappe.PermissionError:
        print(f"You do not have permission to delete Custom DocType {doctype_name}.")

    except Exception as e:
        print(f"Error deleting Custom DocType {doctype_name}: {e}")

def cleanup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, "../config/config.yaml")
    yaml_content = parse(config_file_path)
    roles = yaml_content['roles']
    role_profiles = yaml_content['role_profiles']
    social_login_keys = yaml_content['oidc']['clients']
    role_mappings = yaml_content['role_mappings']
    
    custom_doc_types = ['Social Login Key Extension', 'Role Profile Mapping']

    # cleanup role profile mapping
    for role_profile_mapping in role_mappings:
        cleanup_role_profile_mapping(role_profile_mapping)
        
    # cleanup role profiles
    for role_profile in role_profiles:
        cleanup_role_profile(role_profile)
        
    # cleanup roles
    for role in roles:
        cleanup_role(role)
        
    # cleanup social login keys
    for social_login_key in social_login_keys:
        cleanup_social_login_key(social_login_key)
        
    # cleanup custom doctypes
    for custom_doc_type in custom_doc_types:
        cleanup_custom_doctype(custom_doc_type)