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
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken

    def find(self):
        r"""
        The Get all branches request returns comprehensive information 
        of all the branches available in a particular stack in your account.

        :params limit: {int} -- A limit on the number of objects to return.
        :params skip: {int} -- The number of objects to skip before returning any.
        :params include_count: {bool}
        :return: Returns all the branches
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> branch = client.stack(api_key='api_key').branch()
            >>> response = branch.find()
        --------------------------------
        """
        self.params = {
            "limit": 2,
            "skip": 2,
            "include_count": "false"
        }
        url = f"stacks/branches"
        self.headers['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers, params = self.params)

    def fetch(self):
        r"""
        The Get a single branch request returns information of a specific branch.

        :param branch_uid: {str} -- Unique ID of the branch that is to be fetched.
        :return: Returns the branch of the given UID
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> branch = client.stack(api_key='api_key').branch(branch_uid="branch_uid")
            >>> response = branch.fetch()
        --------------------------------
        """
        url = f"stacks/branches/{self.branch_uid}"
        self.headers['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers)
    
    def create(self, data):
        r"""
        The Create a branch request creates a new branch in a particular stack of your organization.

        :param data: {json} -- Data required in json format to create a branch
        :return: Returns a branch with the given data
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> data = {
                    "branch": {
                    "uid": "release",
                    "source": "main"
                    }
                }
            >>> branch = client.stack(api_key='api_key').branch()
            >>> response = branch.create(data)
        --------------------------------
        """
        url = f"stacks/branches"
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data = data)

    def delete(self):
        r"""
        The Create a branch request creates a new branch in a particular stack of your organization.

        :param branch_uid: {str} -- Unique ID of the branch that is to be deleted.
        :params force: {bool}
        :return: Returns status code and message
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> branch = client.stack(api_key='api_key').branch(branch_uid="branch_uid")
            >>> response = branch.delete(data)
        --------------------------------
        """
        self.params = {
            "force": "true"
        }
        url = f"stacks/branches/{self.branch_uid}?"
        return self.api_client.delete(url, headers = self.headers, params = self.params)
