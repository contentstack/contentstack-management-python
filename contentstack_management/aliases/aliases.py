"""An alias acts as a pointer to a particular branch. You can specify the alias ID in your 
frontend code to pull content from the target branch associated with an alias."""

import json

class Alias:

    """An alias acts as a pointer to a particular branch. You can specify the alias ID in your 
    frontend code to pull content from the target branch associated with an alias."""

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, authorization, alias_uid, data, json_data):
        self.api_client = api_client
        self.endpoint =  endpoint
        self.api_key = api_key
        self.params = {}
        self.headers = headers
        self.authtoken = authtoken
        self.authorization = authorization
        self.alias_uid = alias_uid
        self.data = data
        self.json_data = json_data

    def fetchAll(self):
        r"""
        TThe Get all aliases request returns comprehensive information of all the 
        aliases available in a particular stack in your account..

        :params limit: {int} -- A limit on the number of objects to return.
        :params skip: {int} -- The number of objects to skip before returning any.
        :params include_count: {bool}
        :return: Fetches all the aliases
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> branch = client.stack(api_key='api_key').branchAlias()
            >>> response = branch.fetchAll()
        --------------------------------
        """
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
        r"""
        The Get a single alias request returns information of a specific alias.

        :param branch_alias_uid: {str} -- Unique ID of the alias that is to be fetched.
        :return: Fetches the aliase of the given UID
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> branch = client.stack(api_key='api_key').branchAlias(branch_alias_uid)
            >>> response = branch.fetch()
        --------------------------------
        """
        url = f"stacks/branch_aliases/{self.alias_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        # self.authorization['management_token'] = self.authorization
        return self.api_client.get(url, headers = self.headers)
    
    def assign(self, data):
        r"""
        The Assign an alias request creates a new alias in a particular stack of your organization. 
        This alias can point to any existing branch (target branch) of your stack.

        :param data: {json} -- Data required in json format to assign an alias
        :param alias_uid: {str} -- Unique ID to create and alias
        :return: Assigns an alias with the given data
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> data = {
                    "branch_alias": {
                        "target_branch": "test"
                        }
                    }
            >>> branch = client.stack(api_key='api_key').branchAlias("alias_uid")
            >>> response = branch.assign(data)
        --------------------------------
        """
        url = f"stacks/branch_aliases/{self.alias_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.data = json.dumps(data)
        return self.api_client.put(url, headers = self.headers, data = self.data, json_data = self.json_data)

    def delete(self):
        r"""
        The Delete BranchAlias call is used to delete an existing BranchAlias permanently from your Stack.

        :param alias_uid: {str} -- Unique ID of the alias that is to be deleted.
        :params force: {bool}
        :return: Deletes the alias of the given uid
    
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
        url = f"stacks/branch_aliases/{self.alias_uid}?"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        return self.api_client.delete(url, headers = self.headers, params = self.params)
