import json

class Alias:

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, authorization, branch_alias_uid, data, json_data):
        self.api_client = api_client
        self.endpoint =  endpoint
        self.api_key = api_key
        self.params = {}
        self.headers = headers
        self.authtoken = authtoken
        self.authorization = authorization
        self.branch_alias_uid = branch_alias_uid
        self.data = data
        self.json_data = json_data

    def fetchAll(self):
        self.params = {
            "limit": 2,
            "skip": 2,
            "include_count": "false"
        }
        url = f"stacks/branch_aliases"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        # self.authorization['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers, params = self.params)
    
    def fetch(self):
        url = f"stacks/branch_aliases/{self.branch_alias_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        # self.authorization['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers)
    
    def createOrUpdate(self, branch_uid, data):
        url = f"stacks/branch_aliases/{self.branch_alias_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.data = json.dumps(data)
        return self.api_client.put(url, headers = self.headers, data = self.data, json_data = self.json_data)

    def delete(self):
        self.params = {
            "force": "true"
        }
        url = f"stacks/branch_aliases/{self.branch_alias_uid}?"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        return self.api_client.delete(url, headers = self.headers, params = self.params)
