"""Branches allows you to isolate and easily manage your “in-progress” work 
from your stable, live work in the production environment. 
It helps multiple development teams to work in parallel in a more collaborative,
organized, and structured manner without impacting each other."""

import json

class Branch:

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, authorization, branch_uid, data):
        self.api_client = api_client
        self.endpoint =  endpoint
        self.api_key = api_key
        self.params = {}
        self.headers = headers
        self.authtoken = authtoken
        self.authorization = authorization
        self.branch_uid = branch_uid
        self.data = data

    """
    The Get all branches request returns comprehensive information 
    of all the branches available in a particular stack in your account.
    
    example:
    from contentstack_management import contentstack
    branch = client.stack(api_key='api_key').branch()
    response = branch.find()
    """
    def find(self):
        self.params = {
            "limit": 2,
            "skip": 2,
            "include_count": "false"
        }
        url = f"stacks/branches"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers, params = self.params)

    """
    The Get a single branch request returns information of a specific branch.

    example:
    from contentstack_management import contentstack
    branch = client.stack(api_key='api_key').branch(branch_uid="branch_uid")
    response = branch.fetch()
    """
    def fetch(self):
        url = f"stacks/branches/{self.branch_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers)
    
    def create(self, data):
        url = f"stacks/branches"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data = data)

    def delete(self):
        self.params = {
            "force": "true"
        }
        url = f"stacks/branches/{self.branch_uid}?"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['authorization'] = self.authorization
        return self.api_client.delete(url, headers = self.headers, params = self.params)
