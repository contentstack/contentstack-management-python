from enum import Enum
import os
import pyotp
from ._api_client import _APIClient
from contentstack_management.organizations import organization
from contentstack_management.stack import stack
from contentstack_management.user_session import user_session
from contentstack_management.users import user
from contentstack_management.oauth.oauth_handler import OAuthHandler

version = '0.0.1'


class Region(Enum):
    US = "us"
    EU = "eu"
    AU = "au"
    AZURE_EU = "azure-eu"
    AZURE_NA = "azure-na"
    GCP_NA = "gcp-na"
    GCP_EU = "gcp-eu"


def user_agents(headers=None):
    if headers is None:
        headers = {}
    local_headers = {'X-User-Agent': f'contentstack-management-python/v{version}',
                     "Content-Type": "application/json"}
    headers.update(local_headers)
    return headers


class Client:

    # TODO: DefaultCSCredential(), needs to be implemented
    def __init__(self, host: str = 'api.contentstack.io', scheme: str = 'https://',
                 authtoken: str = None , management_token=None, headers: dict = None,
                 region: Region = Region.US.value, version='v3', timeout=2, max_retries: int = 18, early_access: list = None,
                 oauth_config: dict = None, **kwargs):
        self.endpoint = 'https://api.contentstack.io/v3/'
        
        if region is not None and region is not Region.US.value:
            if host is not None and host != 'api.contentstack.io':
                self.endpoint = f'{scheme}{region}-api.{host}/{version}/'
            else:
                host = 'api.contentstack.com'
                self.endpoint = f'{scheme}{region}-{host}/{version}/'
        elif host is not None and host != 'api.contentstack.io':
            self.endpoint = f'{scheme}{host}/{version}/'
        if headers is None:
            headers = {}
        if early_access is not None:
            early_access_str = ', '.join(early_access)
            headers['x-header-ea'] = early_access_str

        if authtoken is not None:
            headers['authtoken'] = authtoken
        
        if management_token is not None:
            headers['authorization'] = management_token
        headers = user_agents(headers)
        self.client = _APIClient(endpoint=self.endpoint, headers=headers, timeout=timeout, max_retries=max_retries)
        
        # Initialize OAuth if configuration is provided
        self.oauth_handler = None
        if oauth_config:
            self.oauth_handler = OAuthHandler(
                app_id=oauth_config.get('app_id'),
                client_id=oauth_config.get('client_id'),
                redirect_uri=oauth_config.get('redirect_uri'),
                response_type=oauth_config.get('response_type', 'code'),
                client_secret=oauth_config.get('client_secret'),
                scope=oauth_config.get('scope'),
                api_client=self.client
            )

        """
        :param host: Optional hostname for the API endpoint.
        :param authtoken: Optional authentication token for API requests
        :param headers: Optional headers to be included with API requests
        :param authorization: Optional headers to be included in the api request
        :param region: optional region to be included in API requests, 
        We have region support options for na, eu, azure-eu, azure-na
        :param scheme: optional scheme to be included in API requests
        :param version: optional version to be included in API request path url,
        :param timeout: Optional timeout value for API requests
        :param max_requests:Optional maximum number of requests to be made
        :param retry_on_error: Optional boolean value indicating whether to retry API requests on error.
        :return: A client object for performing API operations.
        -------------------------------
        [Example:]

        >>> import contentstack_management
        >>> contentstack_client = contentstack_management.Client()
        -------------------------------
        """

    def login(self, email: str, password: str, tfa_token: str = None, mfa_secret: str = None):
        """
        Login to Contentstack with optional TOTP support.
        
        :param email: User's email address
        :param password: User's password
        :param tfa_token: Optional two-factor authentication token
        :param mfa_secret: Optional MFA secret for automatic TOTP generation. 
                          If not provided, will check MFA_SECRET environment variable
        :return: Response object from the login request
        """
        final_tfa_token = tfa_token
        
        if not mfa_secret:
            mfa_secret = os.getenv('MFA_SECRET')
        
        if mfa_secret and not tfa_token:
            final_tfa_token = self._generate_totp(mfa_secret)
        
        return user_session.UserSession(self.client).login(email, password, final_tfa_token)

    def _generate_totp(self, secret: str) -> str:
        """
        Generate a Time-Based One-Time Password (TOTP) from the provided secret.
        
        :param secret: The MFA secret key for TOTP generation
        :return: The current TOTP code as a string
        """
        totp = pyotp.TOTP(secret)
        return totp.now()

    def logout(self):
        return user_session.UserSession(client=self.client).logout()

    @property
    def authtoken(self):
        return self.client.headers['authtoken']

    def user(self):
        return user.User(self.client)

    def organizations(self, organization_uid: str = None):
        return organization.Organization(self.client, organization_uid)

    def stack(self, api_key: str = None):
        return stack.Stack(self.client, api_key)
    
    def oauth(self, app_id: str, client_id: str, redirect_uri: str, 
              response_type: str = "code", client_secret: str = None, 
              scope: list = None):
        """
        Create an OAuth handler for OAuth 2.0 authentication.
        
        Args:
            app_id: Your registered App ID
            client_id: Your OAuth Client ID
            redirect_uri: The URL where the user is redirected after login and consent
            response_type: OAuth response type (default: "code")
            client_secret: Client secret for standard OAuth flows (optional for PKCE)
            scope: Permissions requested (optional)
            
        Returns:
            OAuthHandler instance
            
        Example:
            >>> import contentstack_management
            >>> client = contentstack_management.Client()
            >>> oauth_handler = client.oauth(
            ...     app_id='your-app-id',
            ...     client_id='your-client-id',
            ...     redirect_uri='http://localhost:3000/callback'
            ... )
            >>> auth_url = oauth_handler.authorize()
            >>> from contentstack_management._messages import OAUTH_VISIT_URL_TO_AUTHORIZE
            >>> print(OAUTH_VISIT_URL_TO_AUTHORIZE.format(auth_url=auth_url))
        """
        return OAuthHandler(
            app_id=app_id,
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
            client_secret=client_secret,
            scope=scope,
            api_client=self.client
        )
