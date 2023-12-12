import contentstack_management
from enum import Enum
from ._api_client import _APIClient
from contentstack_management.organizations import organization
from contentstack_management.stack import stack
from contentstack_management.user_session import user_session
from contentstack_management.users import user

version = '0.0.1'


class Region(Enum):
    US = "us"
    EU = "eu"
    AZURE_EU = "azure-eu"
    AZURE_NA = "azure-na"


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
                 region: Region = Region.US.value, version='v3', timeout=2, max_retries: int = 18,
                 **kwargs):
        self.endpoint = 'https://api.contentstack.io/v3/'
        if region is not None and host is not None and region is not Region.US.value:
            self.endpoint = f'{scheme}{region}-{host}/{version}/'
        if host is not None and region is None:
            self.endpoint = f'{scheme}{host}/{version}/'
        if headers is None:
            headers = {}
        if authtoken is not None:
            headers['authtoken'] = authtoken
        
        if management_token is not None:
            headers['authorization'] = management_token
        headers = user_agents(headers)
        self.client = _APIClient(endpoint=self.endpoint, headers=headers, timeout=timeout, max_retries=max_retries)

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

    def login(self, email: str, password: str, tfa_token: str = None):
        return user_session.UserSession(self.client).login(email, password, tfa_token)
        pass

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
