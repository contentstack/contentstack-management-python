"""Branches allows you to isolate and easily manage your “in-progress” work 
from your stable, live work in the production environment. 
It helps multiple development teams to work in parallel in a more collaborative,
organized, and structured manner without impacting each other."""

import json

from contentstack_management.common import Parameter

_path = 'stacks/branches'


class Branch(Parameter):

    def __init__(self, client, branch_uid=None):
        self.branch_uid = branch_uid
        self.client = client
        super().__init__(self.client)

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
            
            >>> import contentstack_management
            >>> branch = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').branch()
            >>> response = branch.find()
        --------------------------------
        """
        return self.client.get(_path, headers=self.client.headers, params=self.params)

    def fetch(self):
        r"""
        The Get a single branch request returns information of a specific branch.

        :param branch_uid: {str} -- Unique ID of the branch that is to be fetched.
        :return: Returns the branch of the given UID
    
        --------------------------------

        [Example:]
            
            >>> import contentstack_management
            >>> branch = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').branch(branch_uid="branch_uid")
            >>> response = branch.fetch()
        --------------------------------
        """
        if self.branch_uid is None or '':
            raise Exception('branch_uid is required field')
        url = f"{_path}/{self.branch_uid}"
        return self.client.get(url, headers=self.client.headers, params=self.params)

    def create(self, data):
        r"""
        The Create a branch request creates a new branch in a particular stack of your organization.

        :param data: {json} -- Data required in json format to create a branch
        :return: Returns a branch with the given data
    
        --------------------------------

        [Example:]
            
            >>> import contentstack_management
            >>> data = {
                    "branch": {
                    "uid": "release",
                    "source": "main"
                    }
                }
            >>> branch = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').branch()
            >>> response = branch.create(data)
        --------------------------------
        """
        data = json.dumps(data)
        return self.client.post(_path, headers=self.client.headers, data=data, params=self.params)

    def delete(self):
        r"""
        The Create a branch request creates a new branch in a particular stack of your organization.
        :param branch_uid: {str} -- Unique ID of the branch that is to be deleted.
        :params force: {bool}
        :return: Returns status code and message
    
        --------------------------------

        [Example:]
            
            >>> import contentstack_management
            >>> branch = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').branch(branch_uid="branch_uid")
            >>> response = branch.delete(data)
        --------------------------------
        """
        if self.branch_uid is None or '':
            raise Exception('branch_uid is required field')
        url = f"{_path}/{self.branch_uid}"
        return self.client.delete(url, headers=self.client.headers, params=self.params)
