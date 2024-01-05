import frappe
from frappe.model.document import Document

class RoleProfileMapping(Document):
    def before_save(self):
        # check if a document exists with unique fields
        try: 
            existing_role_profile_mapping = frappe.get_doc("Role Profile Mapping", {"social_login_key_name": self.social_login_key_name, "role_profile": self.role_profile})
            if "name" in existing_role_profile_mapping: 
                raise Exception(f"An existing record exists for social login key {self.social_login_key_name} and role_profile {self.role_profile}")
        except Exception as e:
            # Raise a FrappeValidationError to display the error to the user
            frappe.throw(frappe._("An error occurred: {0}").format(e), title=frappe._("Custom Exception"))