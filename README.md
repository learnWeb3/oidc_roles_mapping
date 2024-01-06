## Oidc Roles Mapping

Adding OIDC roles mapping capabilities to Social Login Key DocType.

## How does it works ?

This custom frappe application leverages overrides and custom doctypes to provide extension to the Social Login Key core doctype as well as Role Profile Mappings allowing to map Role Profile to Social Login Key with a role claim extracted from the access token provided by your configured OIDC provider.

This custom frappe application uses a config.yaml file located at: /apps/oidc_roles_mapping/oidc_roles_mapping/config/config.yaml, to perform setup operations on app installation, leaving the administrator the task to enable the configured social login key from the admin web interface 

Here is the format of the config.yaml file with some explanations.

```yaml
oidc:
  clients: # OIDC client list
    - name:  \"keycloak\" # provider name
      enable: 1 # not evaluated for the moment you must activate your client manually
      social_login_provider: \"Custom\" # Leave it like this 
      client_id: \"<OIDC CLIENT ID>\" # OIDC client id
      client_secret: \"<OIDC CLIENT SECRET\" # OIDC client secret
      base_url: \"<KEYCLOAK BASE URL>/realms/<REALM_NAME>\" # OIDC SERVER ROOT URL (eg: Keycloak realm url)
      base64icon: \"\"  # An icon for the social provider loggin button in frappe
      allow_sign_up: 1 # Allow user to sign up 
      authorize_uri: \"/protocol/openid-connect/auth\" # authorize uri of your OIDC provider
      access_token_uri: \"/protocol/openid-connect/token\" # access token uri of your OIDC provider
      redirect_url: \"http://<FRAPPE SITE URL>/api/method/frappe.integrations.oauth2_logins.custom/keycloak\" # redirect url to execute custom oidc logic, leave it like that
      api_endpoint: \"<KEYCLOAK BASE URL>/realms/<REALM_NAME>/protocol/openid-connect/userinfo\" # userinfo endpoint of of your OIDC provider - this must be a valid url
      api_endpoint_args: \"\"# payload to be sent when calling the api_endpoint
      auth_url_data: "{\"response_type\": \"code\", \"scope\": \"openid profile email\"}" # payload to be sent when calling the authorize_uri
      user_claim: \"email\" # user claim name in the access token provided by your OIDC provider
      role_claim: \"realm_access.roles\" # role claim name in the access token provided by your OIDC provider in the form of a json path
      secret_key: \"\" # secret key for offline token validation when calling api
      audience: \"<YOUR AUDIENCE>\" # audience to be validated
      encryption_algorithms: 'RS256' # secret key encryption algorithms RS256,HS256 default is RS256 
      given_name_claim: \"given_name\" # user firstname access token claim used for signup if enable and user does not exists yet
      family_name_claim: \"family_name\" # user lastname access token claim used for signup if enable and user does not exists yet
roles: 
  - name: Invoice Manager 
    rights: 
      - doc_type: <CUSTOM ROLE NAME TO BE CREATED ON APP INSTALL>
        permissions: 
          read: 1
          write: 1
          create: 1
          delete: 1
          submit: 1
          cancel: 1
          amend: 1
          print: 1
          email: 1
          report: 1
          import: 1
          export: 1
          share: 1

role_profiles:
  - name: <CUSTOM ROLE PROFILE NAME TO BE CREATED>
    roles: 
      - <ANY CUSTOM ROLE OR FRAPPE/ERPNEXT ROLE>

  - name: <CUSTOM ROLE PROFILE NAME TO BE CREATED>
    roles: 
      - \"Academics User\"
      - \"Accounts Manager\"
      - \"Accounts User\"
      - \"Agriculture Manager\"
      - \"Agriculture User\"
      - \"Analytics\"
      - \"Auditor\"
      - \"Blogger\"
      # - \"Customer\"
      - \"Dashboard Manager\"
      - \"Delivery Manager\"
      - \"Delivery User\"
      # - \"Employee\"
      - \"Fleet Manager\"
      - \"Fulfillment User\"
      - \"HR Manager\"
      - \"HR User\"
      - \"Inbox User\"
      # - \"Invoice Manager\"
      - \"Item Manager\"
      - \"Knowledge Base Contributor\"
      - \"Knowledge Base Editor\"
      - \"Maintenance Manager\"
      - \"Maintenance User\"
      - \"Manufacturing Manager\"
      - \"Manufacturing User\"
      - \"Newsletter Manager\"
      - \"Prepared Report User\"
      - \"Projects Manager\"
      - \"Projects User\"
      - \"Purchase Manager\"
      - \"Purchase Master Manager\"
      - \"Purchase User\"
      - \"Quality Manager\"
      - \"Report Manager\"
      - \"Sales Manager\"
      - \"Sales Master Manager\"
      - \"Sales User\"
      - \"Script Manager\"
      - \"Stock Manager\"
      - \"Stock User\"
      # - \"Supplier\"
      - \"Support Team\"
      - \"System Manager\"
      - \"Translator\"
      - \"Website Manager\"
      - \"Workspace Manager\"

role_mappings: 
  - name: <MAPPING NAME>
    role_profile: <ROLE PROFILE>
    role_claim_value: <ROLE FROM TOKEN THAT WILL BE EXTRACTED>
    client: \"<CLIENT NAME AKA OIDC.CLIENTS FROM THIS CONFIG FILE>\"
    power: 10 # The greatest powered Role Profile Mapping which is  matching the role claim value in the roles claim of the access token will be used to associate the authenticated user to a Role Profile
```

## Get started

```bash
# fetch app files
bench get-app --branch develop git@github.com:antoineleguillou/oidc_roles_mapping.git --resolve-deps
# create a config file at /apps/oidc_roles_mapping/oidc_roles_mapping/config/config.yaml
# from your bench directory you can do the following command
touch /apps/oidc_roles_mapping/oidc_roles_mapping/config/config.yaml 
echo "
oidc:
  clients: # OIDC client list
    - name:  \"keycloak\" # provider name
      enable: 1 # not evaluated for the moment you must activate your client manually
      social_login_provider: \"Custom\" # Leave it like this 
      client_id: \"<OIDC CLIENT ID>\" # OIDC client id
      client_secret: \"<OIDC CLIENT SECRET\" # OIDC client secret
      base_url: \"<KEYCLOAK BASE URL>/realms/<REALM_NAME>\" # OIDC SERVER ROOT URL (eg: Keycloak realm url)
      base64icon: \"\"  # An icon for the social provider loggin button in frappe
      allow_sign_up: 1 # Allow user to sign up 
      authorize_uri: \"/protocol/openid-connect/auth\" # authorize uri of your OIDC provider
      access_token_uri: \"/protocol/openid-connect/token\" # access token uri of your OIDC provider
      redirect_url: \"http://<FRAPPE SITE URL>/api/method/frappe.integrations.oauth2_logins.custom/keycloak\" # redirect url to execute custom oidc logic, leave it like that
      api_endpoint: \"<KEYCLOAK BASE URL>/realms/<REALM_NAME>/protocol/openid-connect/userinfo\" # userinfo endpoint of of your OIDC provider - this must be a valid url
      api_endpoint_args: \"\"# payload to be sent when calling the api_endpoint
      auth_url_data: "{\"response_type\": \"code\", \"scope\": \"openid profile email\"}" # payload to be sent when calling the authorize_uri
      user_claim: \"email\" # user claim name in the access token provided by your OIDC provider
      role_claim: \"realm_access.roles\" # role claim name in the access token provided by your OIDC provider in the form of a json path
      secret_key: \"\" # secret key for offline token validation when calling api
      audience: \"<YOUR AUDIENCE>\" # audience to be validated
      encryption_algorithms: 'RS256' # secret key encryption algorithms RS256,HS256 default is RS256
      given_name_claim: \"given_name\" # user firstname access token claim used for signup if enable and user does not exists yet
      family_name_claim: \"family_name\" # user lastname access token claim used for signup if enable and user does not exists yet
roles: 
  - name: Invoice Manager 
    rights: 
      - doc_type: <CUSTOM ROLE NAME TO BE CREATED ON APP INSTALL>
        permissions: 
          read: 1
          write: 1
          create: 1
          delete: 1
          submit: 1
          cancel: 1
          amend: 1
          print: 1
          email: 1
          report: 1
          import: 1
          export: 1
          share: 1

role_profiles:
  - name: <CUSTOM ROLE PROFILE NAME TO BE CREATED>
    roles: 
      - <ANY CUSTOM ROLE OR FRAPPE/ERPNEXT ROLE>

  - name: <CUSTOM ROLE PROFILE NAME TO BE CREATED>
    roles: 
      - \"Academics User\"
      - \"Accounts Manager\"
      - \"Accounts User\"
      - \"Agriculture Manager\"
      - \"Agriculture User\"
      - \"Analytics\"
      - \"Auditor\"
      - \"Blogger\"
      # - \"Customer\"
      - \"Dashboard Manager\"
      - \"Delivery Manager\"
      - \"Delivery User\"
      # - \"Employee\"
      - \"Fleet Manager\"
      - \"Fulfillment User\"
      - \"HR Manager\"
      - \"HR User\"
      - \"Inbox User\"
      # - \"Invoice Manager\"
      - \"Item Manager\"
      - \"Knowledge Base Contributor\"
      - \"Knowledge Base Editor\"
      - \"Maintenance Manager\"
      - \"Maintenance User\"
      - \"Manufacturing Manager\"
      - \"Manufacturing User\"
      - \"Newsletter Manager\"
      - \"Prepared Report User\"
      - \"Projects Manager\"
      - \"Projects User\"
      - \"Purchase Manager\"
      - \"Purchase Master Manager\"
      - \"Purchase User\"
      - \"Quality Manager\"
      - \"Report Manager\"
      - \"Sales Manager\"
      - \"Sales Master Manager\"
      - \"Sales User\"
      - \"Script Manager\"
      - \"Stock Manager\"
      - \"Stock User\"
      # - \"Supplier\"
      - \"Support Team\"
      - \"System Manager\"
      - \"Translator\"
      - \"Website Manager\"
      - \"Workspace Manager\"

role_mappings: 
  - name: <MAPPING NAME>
    role_profile: <ROLE PROFILE>
    role_claim_value: <ROLE FROM TOKEN THAT WILL BE EXTRACTED>
    client: \"<CLIENT NAME AKA OIDC.CLIENTS FROM THIS CONFIG FILE>\"
    power: 10 # The greatest powered Role Profile Mapping which is  matching the role claim value in the roles claim of the access token will be used to associate the authenticated user to a Role Profile
" >> /apps/oidc_roles_mapping/oidc_roles_mapping/config/config.yaml
# install app
bench install-app oidc_roles_mapping
# uninstall app
bench uninstall-app oidc_roles_mapping -y
```

#### License

mit