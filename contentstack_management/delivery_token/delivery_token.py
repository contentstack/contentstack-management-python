"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class DeliveryToken(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, delivery_token_uid: str):
        self.client = client
        self.delivery_token_uid = delivery_token_uid
        super().__init__(self.client)

        self.path = "stacks/delivery_tokens"

    def find(self):
        """
        The "Get all delivery tokens" request returns the details of all the delivery tokens created in a stack.
        :return: Json, with delivery_token details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").delivery_token().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
    def fetch(self):
        """
        The "Get a single delivery token" request returns the details of all the delivery tokens created in a stack.
        :return: Json, with delivery_token details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').delivery_token('delivery_token_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.delivery_token_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Create delivery token request creates a delivery token in the stack.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with delivery_token details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "token":{
            >>>            "name":"Test",
            >>>            "description":"This is a demo token.",
            >>>            "scope":[
            >>>                {
            >>>                    "module":"environment",
            >>>                    "environments":[
            >>>                        "production"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
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
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').delivery_token().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params=self.params)
    
    def update(self, data: dict):
        """
        The "Update delivery token" request lets you update the details of a delivery token.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated delivery_token details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "token":{
            >>>            "name":"Test",
            >>>            "description":"This is a updated token.",
            >>>            "scope":[
            >>>                {
            >>>                    "module":"environment",
            >>>                    "environments":[
            >>>                        "production"
            >>>                    ],
            >>>                    "acl":{
            >>>                        "read":true
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
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').delivery_token("delivery_token_uid").update(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.delivery_token_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params=self.params)
    
    
    def delete(self):
        """
        The "Delete delivery token" request deletes a specific delivery token.

        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').delivery_token('delivery_token_uid').delete().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.delivery_token_uid}"
        return self.client.delete(url, headers = self.client.headers, params=self.params)
        
    def validate_uid(self):
         if self.delivery_token_uid is None or '':
            raise ArgumentException("Delivery Token Uid is required")