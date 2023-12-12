"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Roles(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, role_uid: str):
        self.client = client
        self.role_uid = role_uid
        super().__init__(self.client)

        self.path = "roles"

    def find(self):
        """
        The "Get all roles" request returns comprehensive information about all roles created in a stack.
        :return: Json, with roles details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").roles().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The "Get a single role" request returns comprehensive information on a specific role.
        :return: Json, with roles details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').roles('role_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.role_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Create roles request lets you create role of your stack.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with roles details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "role":{
            >>>            "name":"testRole",
            >>>            "description":"This is a test role.",
            >>>            "rules":[
            >>>            {
            >>>                "module":"branch",
            >>>                "branches":[
            >>>                "main"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"branch_alias",
            >>>                "branch_aliases":[
            >>>                "deploy"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"content_type",
            >>>                "content_types":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "sub_acl":{
            >>>                    "read":true
            >>>                }
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"asset",
            >>>                "assets":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "update":true,
            >>>                "publish":true,
            >>>                "delete":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"folder",
            >>>                "folders":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "sub_acl":{
            >>>                    "read":true
            >>>                }
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"environment",
            >>>                "environments":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"locale",
            >>>                "locales":[
            >>>                "en-us"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            }
            >>>            ]
            >>>        }
            >>>        }

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').roles().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The "Update role" request lets you modify an existing role of your stack. However, 
        the pre-existing system roles cannot be modified.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated roles details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "role":{
            >>>            "name":"sampleRole",
            >>>            "description":"This is a test role.",
            >>>            "rules":[
            >>>            {
            >>>                "module":"branch",
            >>>                "branches":[
            >>>                "main"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"branch_alias",
            >>>                "branch_aliases":[
            >>>                "deploy"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"content_type",
            >>>                "content_types":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "sub_acl":{
            >>>                    "read":true
            >>>                }
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"asset",
            >>>                "assets":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "update":true,
            >>>                "publish":true,
            >>>                "delete":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"folder",
            >>>                "folders":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true,
            >>>                "update":true,
            >>>                "publish":true,
            >>>                "delete":true,
            >>>                "sub_acl":{
            >>>                    "read":true,
            >>>                    "update":true,
            >>>                    "publish":true,
            >>>                    "delete":true
            >>>                }
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"environment",
            >>>                "environments":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            },
            >>>            {
            >>>                "module":"locale",
            >>>                "locales":[
            >>>                "$all"
            >>>                ],
            >>>                "acl":{
            >>>                "read":true
            >>>                }
            >>>            }
            >>>            ],
            >>>            "uid":"blt5a570885da41c710"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').roles("role_uid").update(data).json()

        -------------------------------
        """
        
        self.validate_uid()
        url = f"{self.path}/{self.role_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The "Delete role" call deletes an existing role from your stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').roles('role_uid').delete().json()

        -------------------------------
        """
        
        
        self.validate_uid()
        url = f"{self.path}/{self.role_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def validate_uid(self):
        if self.role_uid is None or '':
            raise ArgumentException('Role Uid is required')
    