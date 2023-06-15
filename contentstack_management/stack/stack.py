"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..branches.branches import Branch
from ..aliases.aliases import Alias
from ..content_types.content_type import ContentType

class Stack:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, authorization):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.api_key = api_key
        self.authorization = authorization

    def fetch(self):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    
    def all(self):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)
    
    def create(self, organization_uid, data):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        self.headers['organization_uid'] = organization_uid
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)
    
    def update(self, data):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.put(url, headers = self.headers, data=data)
    
    def delete(self):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.delete(url, headers = self.headers)
    
    def fetch_all_user(self):
        url = "stacks/users"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    
    def update_user_role(self, data):
        url = "stacks/users/roles"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.put(url, headers = self.headers, data=data)
    
    def stack_transfer_ownership(self, data):
        url = "stacks/transfer_ownership"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)
    
    def accept_ownership(self, user_id, ownership_token):
        url = f"stacks/accept_ownership/{ownership_token}"
        self.headers['authtoken'] = self.authtoken
        params = {'api_key': self.api_key, 'uid': user_id}
        return self.api_client.get(url, headers = self.headers, params = params)
    
    def get_stack_settings(self):
        url = "stacks/settings"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    

    def create_stack_settings(self, data):
        url = "stacks/settings"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)

    def reset_stack_settings(self, data):
        url = "stacks/settings/reset"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)
    
    def share_stack(self, data):
        url = "stacks/share"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)
    
    def unshare_stack(self, data):
        url = "stacks/share"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)


    def branch(self, branch_uid = None, data = None):
        data = json.dumps(data)
        return Branch(self.endpoint, self.authtoken, self.headers, self.api_client, self.api_key, self.authorization, branch_uid, data)
    
    def branchAlias(self, alias_uid = None, data = None, json_data = None):
        data = json.dumps(data)
        return Alias(self.endpoint, self.authtoken, self.headers, self.api_client, self.api_key, self.authorization, alias_uid, data, json_data)
    
    def content_type(self, content_type_uid = None, branch = None):
        return ContentType(self.endpoint, self.authtoken, self.headers, self.api_client, self.api_key, self.authorization, branch, content_type_uid)