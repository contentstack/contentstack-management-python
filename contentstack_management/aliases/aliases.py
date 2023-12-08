"""An alias acts as a pointer to a particular branch. You can specify the alias ID in your 
frontend code to pull content from the target branch associated with an alias."""

import json
from ..common import Parameter
_path = 'stacks/branch_aliases'


class Alias(Parameter):
    """An alias acts as a pointer to a particular branch. You can specify the alias ID in your
    frontend code to pull content from the target branch associated with an alias."""

    def __init__(self, client, alias_uid=None):
        self.client = client
        self.alias_uid = alias_uid
        super().__init__(self.client)

    def find(self):
        r"""
        The Get all aliases request returns comprehensive information of all the 
        aliases available in a particular stack in your account.
        :params limit: {int} -- A limit on the number of objects to return.
        :params skip: {int} -- The number of objects to skip before returning any.
        :params include_count: {bool}
        :return: Returns all the aliases
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> alias = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').alias()
            >>> response = alias.find()
        --------------------------------
        """
        return self.client.get(_path, headers=self.client.headers, params=self.params)

    def fetch(self):
        r"""
        The Get a single alias request returns information of a specific alias.

        :return: Returns the aliase of the given UID
    
        --------------------------------

        [Example:]
            >>> import contentstack_management
            >>> alias = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').alias('alias_uid')
            >>> response = alias.fetch()
        --------------------------------
        """
        if self.alias_uid is None or '':
            raise Exception('alias_uid is required')
        url = f"{_path}/{self.alias_uid}"
        return self.client.get(url, headers=self.client.headers, params=self.params)

    def assign(self, data):
        r"""
        The Assign an alias request creates a new alias in a particular stack of your organization. 
        This alias can point to any existing branch (target branch) of your stack.

        :param data: {json} -- Data required in json format to assign an alias
        :return: Returns an alias with the given data
        --------------------------------

        [Example:]
            >>> from contentstack import contentstack
            >>> body = {
            >>>        "branch_alias": {
            >>>            "target_branch": "test"
            >>>            }
            >>>        }
            >>> alias = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').alias("alias_uid")
            >>> response = alias.assign(data)
        --------------------------------
        """
        url = f"{_path}/{self.alias_uid}"
        body = json.dumps(data)
        return self.client.put(url, headers=self.client.headers, params=self.params, data=body)

    def delete(self):
        r"""
        The Delete BranchAlias call is used to delete an existing BranchAlias permanently from your Stack.
        :params force: {bool}
        :return: Returns status code and message
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> alias = contentstack_management.Client(authtoken='your_authtoken').stack(api_key='api_key').alias(alias_uid="alias_uid")
            >>> response = alias.delete()
        --------------------------------
        """
        url = f"{_path}/{self.alias_uid}"
        return self.client.delete(url, headers=self.client.headers, params=self.params)
