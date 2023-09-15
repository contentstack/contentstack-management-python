import os

from dotenv import load_dotenv

# Default config values for running unit tests, provides ease of access to credentials
default_username_value = "cma@contentstack.com"  # Default username value
default_password_value = "cma@contentstack.com"  # Default password value
default_host_value = "api.contentstack.io"  # Default host value
default_organization_uid_value = "orgcontentstack"  # Default organization UID value
default_api_key = "apikeycontentstack"  # API key value
default_authtoken_value = "authtoken@contentstack"  # Default auth token value
default_management_token_value = "management@contentstack"  # Default management token value
default_uid_value = "blt98998999999"  # Default UID value
default_activation_token = "activation@contentstack"  # Default activation token value
default_ownership_token = "ownership@contentstack"  # Default ownership token value
default_user_id = "userid@contentstack"  # Default user uid value
default_content_type_uid = "content_type_uid"  # Default content type  value
default_entry_uid = "entry_uid"  # Default entry value
default_alias_uid = "alias_uid"  # Default alias  value
default_branch_uid = "branch_uid"  # Default branch  value
default_branch_alias_uid = "branch_alias_uid"  # Default branch alias token value
default_global_field_uid = "global_field_uid"  # Default branch alias token value
default_webhook_execution_uid = "webhook_execution_uid"  # Default webhook execution value
default_webhook_uid = "webhook_uid"  # Default webhook value
default_user_id = "userid@contentstack"  # Default ownership token value
default_asset_uid = "asset_uid" #Default asset uid
default_folder_uid = "folder_uid" #Default folder uid
default_workflow_uid = "workflow_uid" #Default workflow uid
default_rule_uid = "rule_uid" #Default rule uid
default_metadata_uid = "metadata_uid" #Default metadata uid
default_role_uid = "roles_uid" #Default roles uid
default_log_item_uid = "log_item_uid" #Default roles uid
default_environments_name = "environments_name" #Default environment name
default_locale_code = "locale_code" #Default locale code
default_taxonomy_uid = "taxonomy_uid" #Default taxonomy code
default_label_uid = "label_uid" #Default label code


def get_credentials():
    load_dotenv()
    credentials = {
        "username": os.getenv("USERNAME", default_username_value),  # Retrieve username from environment or use default
        "password": os.getenv("PASSWORD", default_password_value),  # Retrieve password from environment or use default
        "host": os.getenv("HOST", default_host_value),  # Retrieve host from environment or use default
        "api_key": os.getenv("APIKEY", default_api_key),  # Retrieve api_key from environment or use default
        "organization_uid": os.getenv("ORG_UID", default_organization_uid_value),
        # Retrieve organization UID from environment or use default
        "authtoken": os.getenv("AUTHTOKEN", default_authtoken_value),
        # Retrieve auth token from environment or use default
        "management_token": os.getenv("MANAGEMENT_TOKEN", default_management_token_value),
        # Retrieve management token from environment or use default
        "uid": os.getenv("USER_ID", default_uid_value),  # Retrieve UID from environment or use default
        "activation_token": os.getenv("ACTIVATION_TOKEN", default_activation_token),
        # Retrieve activation token from environment or use default
        "ownership_token": os.getenv("OWNERSHIP_TOKEN", default_ownership_token),
        "user_id": os.getenv("USER_ID", default_user_id),
        # Retrieve ownership token from environment or use default
        "content_type_uid": os.getenv("CONTENT_TYPE_UID", default_content_type_uid),
        "entry_uid": os.getenv("ENTRY_UID", default_entry_uid),
        "alias_uid": os.getenv("ALIAS_UID", default_alias_uid),
        "branch_uid": os.getenv("BRANCH_UID", default_branch_uid),
        "branch_alias_uid": os.getenv("BRANCH_ALIAS_UID", default_branch_alias_uid),
        "global_field_uid": os.getenv("GLOBAL_FIELD_UID", default_global_field_uid),
        "webhook_execution_uid": os.getenv("WEBHOOK_EXECUTION_UID", default_webhook_execution_uid),
        "webhook_uid": os.getenv("WEBHOOK_UID", default_webhook_uid),
        "asset_uid": os.getenv("ASSET_UID", default_asset_uid),
        "folder_uid": os.getenv("FOLDER_UID", default_folder_uid),
        "workflow_uid": os.getenv("WORKFLOW_UID", default_workflow_uid),
        "rule_uid": os.getenv("RULE_UID", default_rule_uid),
        "metadata_uid": os.getenv("METADATA_UID", default_metadata_uid),
        "role_uid": os.getenv("ROLE_UID", default_role_uid),
        "log_item_uid": os.getenv("LOG_ITEM_UID", default_log_item_uid),
        "environments_name": os.getenv("ENVIRONMENT_NAME", default_environments_name),
        "locale_code": os.getenv("LOCALE_CODE", default_locale_code),
        "taxonomy_uid": os.getenv("TAXONOMY_UID", default_taxonomy_uid),
        "label_uid": os.getenv("LABEL_UID", default_label_uid),

    }
    return credentials
