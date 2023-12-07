"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Environment(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, environment_name: str):
        self.client = client
        self.environment_name = environment_name
        super().__init__(self.client)

        self.path = "environments"

    def find(self):
        """
        The Get a single environment call returns more details about the specified environment of a stack.
        :return: Json, with environments details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").environments().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Get all environments call fetches the list of all environments available in a stack.
        :return: Json, with environments details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').environments('environment_name').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.environment_name}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Add an environment call will add a publishing environment for a stack.
        :param data: The data parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with environments details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "environment": {
            >>>            "name": "development",
            >>>            "urls": [{
            >>>                "locale": "en-us",
            >>>                "url": "http://example.com/"
            >>>            }]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').environments().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The Update environment call will update the details of an existing publishing environment for a stack.
        :param data: The data parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated environments details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "environment": {
            >>>            "name": "development",
            >>>            "urls": [{
            >>>                "locale": "en-us",
            >>>                "url": "http://example.com/"
            >>>            }]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').environments("environment_name").update(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.environment_name}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete environment call will delete an existing publishing environment from your stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').environments('environment_name').delete().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.environment_name}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
        
    def validate_uid(self):
         if self.environment_name is None or '':
            raise ArgumentException("Environments Uid is required")