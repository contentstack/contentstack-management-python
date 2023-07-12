from enum import Enum

from contentstack_management._api_client import _APIClient
from contentstack_management.organizations.organizations import Organization
from contentstack_management.stack.stack import Stack
from contentstack_management.user_session.user_session import UserSession
from contentstack_management.users.user import User

version = '0.0.1'


class ContentstackRegion(Enum):
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


class ContentstackClient:

    # TODO: DefaultCSCredential(), needs to be implemented
    def __init__(self, host: str = 'api.contentstack.io', scheme: str = 'https://',
                 authtoken=None, management_token=None, headers: {} = None,
                 region: ContentstackRegion = ContentstackRegion.US, version='v3', timeout=2, max_retries: int = 18,
                 **kwargs):
        self.endpoint = 'https://api.contentstack.io/v3/'
        if region is not ContentstackRegion.US:
            self.endpoint = f'{scheme}{region.value}-{host}/{version}/'
        if host is not None:
            self.endpoint = f'{scheme}{host}/{version}/'
        headers['authtoken'] = authtoken
        headers['authorization'] = management_token
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

        >>> from contentstack_management import contentstack
        >>> contentstack_client = contentstack.client()
        -------------------------------
        """

    def login(self, email: str, password: str, tfa_token: str = None):
        return UserSession(self.client).login(email, password, tfa_token)
        pass

    def logout(self):
        return UserSession(client=self.client).logout()

    @property
    def authtoken(self):
        return self.client.headers['authtoken']

    def user(self):
        return User(self.client)

    def organizations(self, organization_uid: str = None):
        return Organization(self.client, organization_uid)

    def stack(self, api_key: str = None):
        return Stack(self.client, api_key)
