
import json

class Organization:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, organization_uid):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.organization_uid = organization_uid

    
    def get(self):
        url = "organizations"
        if self.organization_uid is None:
            url = "organizations"
        else:
            url = f"organizations/{self.organization_uid}"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def get_organization_roles(self):
        url = f"organizations/{self.organization_uid}/roles"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def organization_add_users(self, user_data):
        url = f"organizations/{self.organization_uid}/share"
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(user_data)
        return self.api_client.post(url, headers = self.headers, data = data)
    
    def transfer_organizations_ownership(self, data):
        url = f"organizations/{self.organization_uid}/transfer-ownership"
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data = data)

    
    def organization_stacks(self):
        url = f"organizations/{self.organization_uid}/stacks"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def organization_logs(self):
        url = f"organizations/{self.organization_uid}/logs"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

