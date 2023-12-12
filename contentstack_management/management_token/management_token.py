"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class ManagementToken(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, management_token_uid: str):
        self.client = client
        self.management_token_uid = management_token_uid
        super().__init__(self.client)

        self.path = "stacks/management_tokens"

    def find(self):
        """
        The find request returns the details of all the management tokens generated in a stack.

        :return: Json, with management_token details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").management_token().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Fetch request returns the details of a specific management token generated in a stack.
        :return: Json, with management_token details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').management_token('management_token_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.management_token_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Create request is used to create a management token in a stack. 
        This token provides you with read-write access to the content of your stack.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with management_token details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "token":{
            >>>            "name":"Test Token",
            >>>            "description":"This is a sample management token.",
            >>>            "scope":[
            >>>                {
            >>>                    "module":"content_type",
            >>>                    "acl":{
            >>>                        "read":true,
            >>>                        "write":true
            >>>                    }
            >>>                },
            >>>                {
            >>>                    "module":"branch",
            >>>                    "branches":[
            >>>                        "main",
            >>>                        "development"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
            >>>                    }
            >>>                },
            >>>                {
            >>>                    "module":"branch_alias",
            >>>                    "branch_aliases":[
            >>>                        "deploy",
            >>>                        "release"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
            >>>                    }
            >>>                }
            >>>            ],
            >>>            "expires_on":"2020-12-10",
            >>>            "is_email_notification_enabled":true
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').management_token().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The Update request lets you update the details of a management token. 
        You can change the name and description of the token, update the stack-level permissions assigned to the token, 
        and change the expiry date of the token (if set).

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated management_token details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "token":{
            >>>            "name":"Updated Test Token",
            >>>            "description":"This is an updated management token.",
            >>>            "scope":[
            >>>                {
            >>>                    "module":"content_type",
            >>>                    "acl":{
            >>>                        "read":true,
            >>>                        "write":true
            >>>                    }
            >>>                },
            >>>                {
            >>>                    "module":"entry",
            >>>                    "acl":{
            >>>                        "read":true,
            >>>                        "write":true
            >>>                    }
            >>>                },
            >>>                {
            >>>                    "module":"branch",
            >>>                    "branches":[
            >>>                        "main",
            >>>                        "development"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
            >>>                    }
            >>>                },
            >>>                {
            >>>                    "module":"branch_alias",
            >>>                    "branch_aliases":[
            >>>                        "deploy"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
            >>>                    }
            >>>                }
            >>>            ],
            >>>            "expires_on":"2020-12-31",
            >>>            "is_email_notification_enabled":true
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').management_token("management_token_uid").update(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.management_token_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete request deletes a specific management token.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').management_token('management_token_uid').delete().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.management_token_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def validate_uid(self):
         if self.management_token_uid is None or '':
            raise ArgumentException("Management Token Uid is required")