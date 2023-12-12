import json
from ..common import Parameter


class Organization(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API
    """

    def __init__(self, client, organization_uid):
        self.client = client
        self.organization_uid = organization_uid
        self._path = f'organizations/{self.organization_uid}'
        super().__init__(client)

    def find(self):
        """
        Finds the organizations entries 
        :return: Json, with organizations details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.organizations().find()
        -------------------------------
        """
        return self.client.get('organizations', headers=self.client.headers, params = self.params)

    def fetch(self):
        """
        Fetches the organizations entry
        :return: Json, with organizations details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(host='host', authtoken="")
            
            >>> result = client.organizations('organization_uid').fetch().json()

        -------------------------------
        """
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        return self.client.get(self._path, headers=self.client.headers, params = self.params)

    def roles(self):
        """
        Fetches the organization roles entries 
        :return: Json, with organization role details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.organizations('organization_uid').get_organization_roles().json()

        -------------------------------
        """
        url = f"{self._path}/roles"
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        return self.client.get(url, headers=self.client.headers, params = self.params)

    def add_users(self, user_data):
        """
        Add user to the organization 
        :return: Json, with user details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>            "share": {
            >>>                "users": {
            >>>                    "abc@sample.com": ["{****}"],
            >>>                    "xyz@sample.com": ["{****}"]
            >>>                },
            >>>                "stacks": {
            >>>                    "abc@sample.com": {
            >>>                        "{{apiKey}}": ["{****}"]
            >>>                    },
            >>>                    "xyz@sample.com": {
            >>>                    }
            >>>                },
            >>>                "message": "Invitation message"
            >>>            }
            >>>        }
            >>>
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.organizations('organization_uid').organization_add_users(data).json()
        -------------------------------
        """
        url = f"{self._path}/share"
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        data = json.dumps(user_data)
        return self.client.post(url, headers=self.client.headers, data=data, params = self.params)

    def transfer_ownership(self, data):
        """
        Add user to the organization 
        :return: Json, with user details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>      "transfer_to": "abc@sample.com"
            >>>   }
            >>>
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.organizations('organization_uid').transfer_organizations_ownership(data)
        -------------------------------
        """
        url = f"{self._path}/transfer-ownership"
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        data = json.dumps(data)
        return self.client.post(url, headers=self.client.headers, data=data, params = self.params)

    def stacks(self):
        """
        Fetches the organization stacks 
        :return: Json, with organization stack details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.organizations('organization_uid').organization_stacks()
        -------------------------------
        """
        url = f"{self._path}/stacks"
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        return self.client.get(url, headers=self.client.headers, params = self.params)

    def logs(self):
        """
        Fetches the organization log entries 
        :return: Json, with organization log details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.organizations('organization_uid').organization_logs().json()
        -------------------------------
        """
        url = f"{self._path}/logs"
        if self.organization_uid is None or '':
            raise Exception('organization_uid is required')
        return self.client.get(url, headers=self.client.headers, params=self.params)
