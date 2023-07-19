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
default_user_id = "userid@contentstack"  # Default ownership token value
default_asset_uid = "asset_uid" #Default asset uid
default_folder_uid = "folder_uid" #Default folder uid

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
        "asset_uid": os.getenv("ASSET_UID", default_asset_uid),
        "folder_uid": os.getenv("FOLDER_UID", default_folder_uid),
    }
    return credentials
