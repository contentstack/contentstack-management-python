import platform

import contentstack_management
from ..core.http_client import HttpClient

class Organization:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers

    
    def get_organizations(self):
        url = "organizations"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()


    def get_organization(self, organization_uid):
        url = f"organizations/{organization_uid}"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()
    
    def get_organization_roles(self, organization_uid):
        url = f"organizations/{organization_uid}/roles"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()
    
    def organization_add_users(self, organization_uid):
        url = f"organizations/{organization_uid}/share"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()
    
    def transfer_organizations_onership(self, organization_uid):
        url = f"organizations/{organization_uid}/transfer-ownership"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()
    
    def organization_stacks(self, organization_uid):
        url = f"organizations/{organization_uid}/stacks"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()
    
    def organization_logs(self, organization_uid):
        url = f"organizations/{organization_uid}/logs"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers).json()