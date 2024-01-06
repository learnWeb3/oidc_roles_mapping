import frappe
import jwt

def validate_custom_jwt(**args):
    
    content_type = frappe.request.headers.get("Content-Type", None)
    
    # content-type is not application/json dismiss
    if not content_type == "application/json":
        return 
    
    authorization_header = frappe.request.headers.get('Authorization', None)
    
    if not authorization_header: 
        return error_response(400, message="Missing Authorization header")
    
    token = authorization_header.replace("Bearer ", "")
    
    if not token: 
        return error_response(400, message="Missing Bearer token")
    
    enabled_social_login_keys = frappe.get_list(
        "Social Login Key", 
        filters={"enable_social_login": 1},  
        fields=['provider_name', 'enable_social_login', 'user_id_property'], 
        ignore_permissions=True
    )
    
    # no external providers have been configured dismiss
    if  len(enabled_social_login_keys) == 0:
        return
    
    for enabled_social_login_key in enabled_social_login_keys:
        
        try: 
            social_login_key_extension = frappe.get_last_doc(
                'Social Login Key Extension',  
                filters={
                    'social_login_key_name': enabled_social_login_key['provider_name']
                }
            )
            user_claim_name = enabled_social_login_key.user_id_property or "sub"
            roles_claim_name = social_login_key_extension.role_claim or "roles"
            public_key = f"-----BEGIN PUBLIC KEY-----\n{social_login_key_extension.secret_key}\n-----END PUBLIC KEY-----"
            encryption_algorithms = social_login_key_extension.encryption_algorithms or "RS256"
            
            audience = social_login_key_extension.audience
            decoded_token = jwt.decode(token, public_key, algorithms=[encryption_algorithms], audience=audience)
            email = decoded_token[user_claim_name]
            
            user_exists = frappe.db.exists("User", {"email": email})
            
            if not user_exists:
                raise Exception("User does not exists")
            
            user = frappe.get_doc("User", email)
            
            # Allows making changes on the user (like adding roles) by guest user.
            user.flags.ignore_permissions = True

            if not user.enabled:
                raise Exception("User must be enabled")
            
            role_profile_mapping = get_role_profile_mapping(enabled_social_login_key['provider_name'], decoded_token, roles_claim_name, user )
            
            user.role_profile_name = role_profile_mapping.role_profile
            user.save()
            
            frappe.set_user(user.email)
            
            return True
            
        except Exception as err:
            print(f"JWT Authentication error {err}")
            
    
    return error_response(401, message="You are not authorized to access this resource")


def error_response(http_status_code=401, message="You are not authorized to access this resource"):
    errors_status_map = {
        400: "Bad Request",
        401: "Unauthorized",
        500: "Internal Server Error"
    }

    frappe.local.response['http_status_code'] = http_status_code
    frappe.local.response['message'] = message
    frappe.local.response['status'] = errors_status_map[http_status_code],
    frappe.local.response['type'] = 'json'



def get_role_profile_mapping(provider_name, decoded_token, roles_claim_name, user):
    # Gets the documents of the Role Profile Mapping matching the Social Login Key configuration
    role_profile_mappings = frappe.get_list(
        "Role Profile Mapping", 
        filters={'social_login_key_name': provider_name },  
        fields=['role_claim_value', 'power', 'name', 'role_profile', 'social_login_key_name', 'role_profile_mapping_name'], 
        ignore_permissions=True
    )
    
    # print(role_profile_mappings)
    # create a dict mapping role_claim_value => role_profile_mapping
    role_profile_mappings_claim_value_map = {}
    
    for role_profile_mapping in role_profile_mappings:
        role_profile_mappings_claim_value_map[role_profile_mapping.role_claim_value] = role_profile_mapping
        
    # extract matching Role Profile Mapping to the roles claims in the decoded_token
    matching_role_profile_claim_values = list(
        filter(
            lambda role_claim_value: role_claim_value in role_profile_mappings_claim_value_map, 
            extract_role_claim_value(roles_claim_name, decoded_token)
        )
    )
    
    if not len(matching_role_profile_claim_values):
        frappe.respond_as_web_page(_("Not Allowed"), _("User {0} is disabled").format(user.email))
        return False
    
    # create a dict mapping power => matching_role_profile_mapping
    matching_role_profile_mappings_power_map = {}
    
    for matching_role_profile_claim_value in matching_role_profile_claim_values:
        matching_role_profile_mappings_power_map[role_profile_mappings_claim_value_map[matching_role_profile_claim_value].power] = role_profile_mappings_claim_value_map[matching_role_profile_claim_value]
        
    # user role profile mapping match the last item of the dict
    role_profile_mapping = list(
            matching_role_profile_mappings_power_map.values()
        )[
            len(
                list(
                    matching_role_profile_mappings_power_map.values()
                )
            ) - 1
        ]
    
    print(f"found role profile mapping {role_profile_mapping.role_profile_mapping_name}, role profile is {role_profile_mapping.role_profile}")
    return role_profile_mapping

def extract_role_claim_value(roles_claim_name, decoded_token):
    splitted_claim_name_parts = roles_claim_name.split('.')
    temp = decoded_token
    for splitted_claim_name_part in splitted_claim_name_parts:
        temp = temp[splitted_claim_name_part]
    return temp