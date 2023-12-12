"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException
from ..terms.terms import Terms

class Taxonomy(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, taxonomy_uid: str):
        self.client = client
        self.taxonomy_uid = taxonomy_uid
        super().__init__(self.client)

        self.path = "taxonomies"

    def find(self):
        """
        This call fetches the list of all taxonomies available for a stack.
        :return: Json, with taxonomy details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").taxonomy().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self, taxonomy_uid: str = None):
        """
        The "Get a taxonomy" call returns information about a specific taxonomy available on the stack.
        :return: Json, with taxonomy details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').fetch('taxonomy_uid').json()

        -------------------------------
        """
        if taxonomy_uid is not None and taxonomy_uid != '':
            self.taxonomy_uid = taxonomy_uid
            
        self.validate_taxonomy_uid()
        url = f"{self.path}/{self.taxonomy_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        This call lets you add a new taxonomy to your stack.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with taxonomy details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "taxonomy": {
            >>>            "uid": "taxonomy12345",
            >>>            "name": "Taxonomy 12345",
            >>>            "description": "Description for Taxonomy 1"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict, taxonomy_uid: str = None):
        """
        The "Update taxonomy" call will let you update the details

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated taxonomy details.
        -------------------------------
        [Example:]
            >>> data ={
            >>>    "taxonomy": {
            >>>        "name": "Taxonomy 12345",
            >>>        "description": "Description updated for Taxonomy 12345"
            >>>    }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy("taxonomy_uid").update(data).json()

        -------------------------------
        """
        
        if taxonomy_uid is not None and taxonomy_uid != '':
            self.taxonomy_uid = taxonomy_uid

        self.validate_taxonomy_uid()
        url = f"{self.path}/{self.taxonomy_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self, taxonomy_uid: str = None): 
        """
        The "Delete taxonomy" call deletes an existing taxonomy from your stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').taxonomy('taxonomy_uid').delete('taxonomy_uid').json()

        -------------------------------
        """
        
        if taxonomy_uid is not None and taxonomy_uid != '':
            self.taxonomy_uid = taxonomy_uid
            
        self.validate_taxonomy_uid()
        url = f"{self.path}/{self.taxonomy_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
        
    def validate_taxonomy_uid(self):
        if self.taxonomy_uid is None or '':
            raise ArgumentException('Taxonomy Uid is required')
        
    def terms(self, terms_uid: str = None):
        self.validate_taxonomy_uid()
        return Terms(self.client, self.taxonomy_uid, terms_uid)
        
    
    