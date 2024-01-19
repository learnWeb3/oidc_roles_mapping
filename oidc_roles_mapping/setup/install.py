import frappe
import json
import os.path
from oidc_roles_mapping.setup.yaml_parser  import parse


def after_install():
    setup_oidc_roles_mapping()
 
 

def create_role_if_not_exists(role={
    "name": "Invoice Manager",
    "rights": [
        {
            "doc_type": "Sales Invoice",
            "permissions": {"read": 1, "write": 1, "create": 1}
        }
    ]
}):
    
    try: 
        new_role = frappe.new_doc("Role")
        new_role.update({
            "role_name": role["name"]
        })
        new_role.save()
        create_doc_types_permissions_for_role(role["name"], role['rights'])
        print(f"role {role['name']} created with success")
    except Exception as err:
        print(f"error creating role {role['name']} due to error {err}")
    

def create_doc_types_permissions_for_role(role_name="Invoice Manager", rights=[
        {
            "doc_type": "Sales Invoice",
            "permissions": {"read": 1, "write": 1, "create": 1}
        }
    ]):

    for right in rights:
        try: 
            create_permissions_for_role_and_doctype(role_name, right['doc_type'], right['permissions'])
            print(f"right for doctype {right['doc_type']} created with success")
        except Exception as err:
            print(f"error creating right for doctype {right['doc_type']} due to error {err}")
            

def create_permissions_for_role_and_doctype(role, doctype, permissions):
    try:
       
        doc_perm = frappe.new_doc("Custom DocPerm")
        doc_perm.parent = doctype
        doc_perm.role = role
        doc_perm.permlevel = 0 
        doc_perm.read = permissions.get("read", 0)
        doc_perm.write = permissions.get("write", 0)
        doc_perm.create = permissions.get("create", 0)
        doc_perm.submit = permissions.get("submit", 0)
        doc_perm.cancel = permissions.get("cancel", 0)
        doc_perm.amend = permissions.get("amend", 0)
        doc_perm.print_ = permissions.get("print", 0)
        doc_perm.email = permissions.get("email", 0)
        doc_perm.report = permissions.get("report", 0)
        doc_perm.import_ = permissions.get("import", 0)
        doc_perm.export = permissions.get("export", 0)
        doc_perm.share = permissions.get("share", 0)

        doc_perm.save()
        print(f"DocPerm entry for Role '{role}' on DocType '{doctype}' created successfully.")
    except Exception as err:
        print(f"Error creating DocPerm entry for Role '{role}' on DocType '{doctype}' due to error: {err}")



    
    
    
def create_user_if_not_exists(user={
    "first_name": "webservice",
    "last_name": "webservice",
    "username": "webservice",
    "password": "foobar",
    "roles": [ "webservice"],
    "default_role_profile": "webservice",
}):
    
    roles = []
  
    for role in user['roles']:
        roles.append( {"role": role})

    try: 
        new_user = frappe.new_doc("User")
        new_user.update({
            "email": user['email'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "username": user['username'],
            "roles": roles,
            "role_profile_name": user['default_role_profile'],
            "password": user['password'] # to do generate random password to disable login
        })
        new_user.save()
        print(f"user account with username {user['username']} created with success")
    except Exception as err:
            print(f"error creating user with username {user['username']} due to error {err}")
    
def create_role_profile_if_not_exists(role_profile={
    "name": "webservice",
    "roles": ["Invoice Manager"]
}):
    roles = []
    for role in role_profile['roles']:
        roles.append( {"role": role, "read": 1, "write": 1, "create": 1, "delete": 1},)
    try: 
        new_role_profile = frappe.new_doc("Role Profile")
        new_role_profile.update({
            "role_profile": role_profile['name'],
            "roles": roles
        })
        new_role_profile.save()
        print(f"role profile {role_profile['name']} created with success")
    except Exception as err:
        print(f"error creating role profile {role_profile['name']} due to error {err} type {type(err)}")
    
def create_role_mapping(
    role_profile_mapping={
        "name": "superadmin claim to superadmin role profile",
        "role_profile": "superadmin",
        "role_claim_value": "superadmin",
        "client": "keycloak",
        "power": 10
}): 
    try: 
        new_role_mapping = frappe.new_doc("Role Profile Mapping")
        new_role_mapping.update({
            "role_profile_mapping_name": role_profile_mapping['name'],
            "role_profile": role_profile_mapping['role_profile'],
            "role_claim_value": role_profile_mapping['role_claim_value'],
            "social_login_key_name": role_profile_mapping['client'],
            "power": role_profile_mapping['power']
        })
        new_role_mapping.save()
        print(f"role mapping between role profile {role_profile_mapping['role_profile']} and role claim value {role_profile_mapping['role_claim_value']} created with success")
    except Exception as err:
        print(f"error creating role profile mapping between role profile {role_profile_mapping['role_profile']} and role claim value {role_profile_mapping['role_claim_value']} due to error {err} type {type(err)}")
    

def create_social_login_key(social_login_key={
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
        "given_name_claim": "given_name",
        "family_name_claim": "family_name",
        "secret_key": "",
        "audience": "",
        "encryption_algorithms": 'RS256',
        "service_account_claim": "client_id",
        "service_account_claim_suffix": "@service-account.com"
}):
    
    try: 
        # create social login key
        new_social_login_key = frappe.new_doc("Social Login Key")
        new_social_login_key.update({
            "provider_name":  social_login_key['name'],
            "social_login_provider": social_login_key['social_login_provider'],
            "client_id": social_login_key['client_id'],
            "client_secret": social_login_key['client_secret'],
            "base_url":  social_login_key['base_url'],
            "icon":  social_login_key['base64icon'], # icon
            "sign_ups": "Allow" if social_login_key['allow_sign_up'] == 1 else "Deny", # sign_ups values Allow Deny
            "authorize_url": social_login_key['authorize_uri'], # authorize_url
            "access_token_url": social_login_key['access_token_uri'], # access_token_url
            "redirect_url": social_login_key['redirect_url'],
            "api_endpoint": social_login_key['api_endpoint'],
            "api_endpoint_args": social_login_key['api_endpoint_args'],
            "auth_url_data":social_login_key['auth_url_data'],
            "user_id_property":  social_login_key['user_claim'],  #  user_id_property
        })
        new_social_login_key.save()
        
        # create extensions to handle roles
        new_social_login_key_extension = frappe.new_doc("Social Login Key Extension")
        new_social_login_key_extension.update({
            "social_login_key_extension_name": f"extension for provider {social_login_key['name']}",
            "social_login_key_name": social_login_key['name'],
            "role_claim": social_login_key['role_claim'],
            "audience": social_login_key['audience'],
            "encryption_algorithms": social_login_key['encryption_algorithms'],
            "secret_key": social_login_key['secret_key'],
            "given_name_claim": social_login_key["given_name_claim"],
            "family_name_claim": social_login_key["family_name_claim"],
            "service_account_id_property": social_login_key["service_account_claim"],
            "service_account_id_property_suffix": social_login_key["service_account_claim_suffix"]
        })
        new_social_login_key_extension.save()
        
        # # activate social login key
        # if social_login_key['enable'] == 1:
        #     try: 
        #         social_login_key_to_activate = frappe.get_doc({
        #             "doctype": "Social Login Key",
        #             "provider_name":  social_login_key['name'],
        #         })
        #         social_login_key_to_activate.enable_social_login = 1
        #         social_login_key_to_activate.save()
        #         print(f"social login key {social_login_key['name']} activated with success")
        #     except Exception as err:
        #         print(f"error enabling social login key {social_login_key['name']} due to error {err} type {type(err)}")
    except Exception as err:
        print(f"error creating social login key {social_login_key['name']} due to error {err} type {type(err)}")
        
        
def initialize_social_login_key_extension_doctype():
    try:
        JSON_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(JSON_BASE_DIR, "../doctype/social_login_key_extension/social_login_key_extension.json")
        # Read the JSON file
        with open(FILE_PATH, 'r') as file:
            doctype_definition = json.load(file)

        # Create the DocType
        doc_type = frappe.get_doc(doctype_definition)
        doc_type.insert(ignore_permissions=True)

        print("Social Login Key Extension DocType initialized successfully.")

    except frappe.DuplicateEntryError:
        print("Social Login Key Extension DocType already exists.")

    except Exception as e:
        print(f"Error initializing Social Login Key Extension DocType: {e}")
        
def initialize_role_mapping_doctype():
    try:
        JSON_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(JSON_BASE_DIR, "../doctype/role_profile_mapping/role_profile_mapping.json")
        # Read the JSON file
        with open(FILE_PATH, 'r') as file:
            doctype_definition = json.load(file)

        # Create the DocType
        doc_type = frappe.get_doc(doctype_definition)
        doc_type.insert(ignore_permissions=True)
        print("Role Profile Mapping DocType initialized successfully.")

    except frappe.DuplicateEntryError:
        print("Role Profile Mapping DocType already exists.")

    except Exception as e:
        print(f"Error initializing Role Profile Mapping DocType: {e}")


def setup_oidc_roles_mapping():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, "../config/config.yaml")
    yaml_content = parse(config_file_path)
    roles = yaml_content['roles']
    role_profiles = yaml_content['role_profiles']
    social_login_keys = yaml_content['oidc']['clients']
    role_mappings = yaml_content['role_mappings']
    
    initialize_social_login_key_extension_doctype()
    initialize_role_mapping_doctype()

    # seed roles
    for role in roles:
        create_role_if_not_exists(role)
    
    # seed role profiles
    for role_profile in role_profiles:
        create_role_profile_if_not_exists(role_profile)
        
    # seed social login keys
    for social_login_key in social_login_keys:
        create_social_login_key(social_login_key)
    
    # seed role mapping
    for role_profile_mapping in role_mappings:
        create_role_mapping(role_profile_mapping)
    
        
    
