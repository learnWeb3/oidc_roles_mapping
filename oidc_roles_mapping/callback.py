# Readings:
# - https://github.com/frappe/frappe/blob/828490e01a3d14e1b0ac3385ea196c72ab2cc950/frappe/integrations/oauth2_logins.py
# - https://github.com/frappe/frappe/blob/828490e01a3d14e1b0ac3385ea196c72ab2cc950/frappe/utils/oauth.py
# - https://github.com/castlecraft/microsoft_integration/blob/main/microsoft_integration/callback.py

import json
import base64
import requests
import jwt

import frappe
import frappe.utils
import os.path

#frappe.utils.logger.set_log_level("DEBUG")

@frappe.whitelist(allow_guest=True)
def custom(code: str, state: str | dict):
    """Callback for processing the request received after a successful authentication in an identity provider (OIDC provider).

    OIDC redirect URL: /api/method/oidc_extended.callback.custom/<provider name>

    This extends the functionality of the current Social Login (OIDC) module. In addition to handling the authentication over OIDC, this:
    - Creates new user if does not exsit.
    - Maps role from the claim of access token to ERPNext role profile
    """

    state = json.loads(base64.b64decode(state).decode("utf-8"))
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if not state or not state["token"]:
        frappe.respond_as_web_page(_("Invalid request"), _("Token is missing."), http_status_code=417)
        return

    request_path_components = frappe.request.path[1:].split("/")

    if not len(request_path_components) == 4 or not request_path_components[3]:
        frappe.respond_as_web_page(_("Invalid request"), _("The redirect URL is invalid."), http_status_code=417)
        return

    # Gets the name of the OIDC custom provider.
    provider_name = request_path_components[3]

    # Gets the document of the Social Login Key configuration.
    social_login_provider = frappe.get_doc({"doctype": "Social Login Key", "name": provider_name})
    
    # Gets the document of the Social Login Key Extension matching the Social Login Key  configuration
    social_login_key_extension = frappe.get_doc({'doctype': 'Social Login Key Extension',  'social_login_key_extension_name': provider_name})
    
    # extract claims name
    user_id_claim_name = social_login_provider.user_id_property or "sub"
    roles_claim_name = social_login_key_extension.role_claim or "roles"
    given_name_claim_name = social_login_key_extension.given_name_claim or "given_name"
    family_name_claim_name = social_login_key_extension.family_name_claim or "family_name"
    audience = social_login_key_extension.audience

    token_request_data = {
        "grant_type": "authorization_code",
        "client_id": social_login_provider.client_id,
        "client_secret": social_login_provider.get_password("client_secret"),
        "scope": json.loads(social_login_provider.auth_url_data).get("scope"),
        "code": code,
        "redirect_uri": frappe.utils.get_url(social_login_provider.redirect_url), # Combines ERPNext URL with redirect URL.
    }

    # Requests token from token endpoint.
    token_response = requests.post(
        url=social_login_provider.base_url + social_login_provider.access_token_url,
        data=token_request_data,
    ).json()

    token = jwt.decode(token_response["id_token"], audience, options={"verify_signature": False})
    
    # extract claim values 
    email = token[user_id_claim_name]

    # Creates the user if does not exsit, otherwise updates the data according to the claims of the token.
    if frappe.db.exists("User", {"email": email}):
        # Fetches the existing user.
        user = frappe.get_doc("User", email)
    else:
        user = frappe.get_doc(
            {
                "doctype": "User",
                "first_name": token[given_name_claim_name],
                "last_name": token[family_name_claim_name],
                "email": email,
                "send_welcome_email": 0,
                "enabled": 1,
                "new_password": frappe.generate_hash(),
                "user_type": "System User"
            }
        )
        # Allows making changes on the user (like adding roles) by guest user.
        user.flags.ignore_permissions = True

    if not user.enabled:
        frappe.respond_as_web_page(_("Not Allowed"), _("User {0} is disabled").format(user.email))
        return False

    # if not user.get_social_login_userid(provider_name):
    #     user.set_social_login_userid(provider_name, userid=username)

    # Allows all changes on the user in this code without checking if the operation is permitted to be done by the current user.
    user.flags.ignore_permissions = True
    
    role_profile_mapping = get_role_profile_mapping(provider_name, token, roles_claim_name, user)

    # associate user to its role profile
    user.role_profile_name = role_profile_mapping.role_profile
    user.save()

    frappe.local.login_manager.user = email # The main identity of user used by Frappe is email.
    frappe.local.login_manager.post_login()

    frappe.db.commit()

    redirect_post_login(
        desk_user=frappe.local.response.get("message") == "Logged In",
        redirect_to=state.get("redirect_to")
    )
    
def get_role_profile_mapping(provider_name, token, roles_claim_name, user):
    # Gets the documents of the Role Profile Mapping matching the Social Login Key configuration
    role_profile_mappings = frappe.get_list("Role Profile Mapping", filters={'social_login_key_extension_name': provider_name })
    
    # create a dict mapping role_claim_value => role_profile_mapping
    role_profile_mappings_claim_value_map = {}
    
    for role_profile_mapping in role_profile_mappings:
        role_profile_mappings_claim_value_map[role_profile_mapping.role_claim_value]
        
    # extract matching Role Profile Mapping to the roles claims in the token
    matching_role_profile_mappings = filter(lambda role_claim_value: role_claim_value in role_profile_mappings_claim_value_map, token[roles_claim_name])
    
    if not len(matching_role_profile_mappings):
        frappe.respond_as_web_page(_("Not Allowed"), _("User {0} is disabled").format(user.email))
        return False
    
    # create a dict mapping power => matching_role_profile_mapping
    matching_role_profile_mappings_power_map = {}
    
    for matching_role_profile_mapping in matching_role_profile_mappings:
        matching_role_profile_mappings_power_map[matching_role_profile_mapping.power]
        
    # user role profile mapping match the last item of the dict
    role_profile_mapping = matching_role_profile_mappings_power_map.values()[len(matching_role_profile_mappings_power_map.values()) - 1]
    
    print(f"found role profile mapping {role_profile_mapping.role_profile_mapping_name}, role profile is {role_profile_mapping.role_profile}")
    return role_profile_mapping

def redirect_post_login(desk_user: bool, redirect_to: str):
    frappe.local.response["type"] = "redirect"

    if not redirect_to:
        desk_uri = "/app"
        redirect_to = frappe.utils.get_url(desk_uri if desk_user else "/me")

    frappe.local.response["location"] = redirect_to

