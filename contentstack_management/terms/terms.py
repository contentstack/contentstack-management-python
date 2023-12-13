"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Terms(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, taxonomy_uid: str, terms_uid: str):
        self.client = client
        self.taxonomy_uid = taxonomy_uid
        self.terms_uid = terms_uid
        super().__init__(self.client)
        self.path = f"taxonomies/{self.taxonomy_uid}/terms"

    def find(self):
        """
        This call fetches the list of all terms available for a taxonomies.
        :return: Json, with taxonomy details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").taxonomy("taxonomy_uid").terms().find()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self, terms_uid: str = None):
        """
        The Get a terms call returns information about a specific taxonomy available on the stack.
        
        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        the terms you want to fetch. It is an optional parameter, meaning it can be None or an empty
        string if you don't want to specify a specific terms_uid
        :type terms_uid: str
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').terms('terms_uid').fetch()

        -------------------------------
        """
        
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid
            
        self.validate_taxonomy_uid()
        self.validate_terms_uid()
        url = f"{self.path}/{self.terms_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        This call lets you add a new terms to your taxonomy.
        
        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It will be converted to a JSON string using the `json.dumps()` function before
        being sent in the request
        :type data: dict
        :return: The code is returning the result of the `post` method call on the `self.client` object.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "term": {
            >>>            "uid": "term_1",
            >>>            "name": "Term 1"
            >>>        },
            >>>        "parent_uid": null
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').terms().create(data)
        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict, terms_uid: str = None):
        """
        The function updates a resource with the given data and terms UID.
        
        :param data: A dictionary containing the data to be updated
        :type data: dict
        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        the terms you want to update
        :type terms_uid: str
        :return: the result of the `self.client.put()` method, which is the response from making a PUT
        request to the specified URL with the provided data and headers.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "term": {
            >>>            "name": "Term 1"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy("taxonomy_uid").terms('terms_uid').update(data)

        -------------------------------
        """
        
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid

        self.validate_taxonomy_uid()
        url = url = f"{self.path}/{self.terms_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self, terms_uid: str = None): 
        """
        The Delete terms call deletes an existing terms from your taxonomy.
        
        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        the terms you want to delete
        :type terms_uid: str
        :return: the result of the delete request made to the specified URL.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').taxonomy('taxonomy_uid').terms('terms_uid').delete('taxonomy_uid')

        -------------------------------
        """
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid
            
        self.validate_taxonomy_uid()
        self.validate_terms_uid()
        url = f"{self.path}/{self.terms_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    

    def search(self, term_string: str):
        """
        The "Get a terms" call returns information about a specified terms available on the taxonomy.
        
        :param term_string: The term_string parameter is a string that represents the term you want to
        search for. It is used to specify the term you want to search for in the search function
        :type term_string: str
        :return:Json, with taxonomy details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').terms('terms_uid').search("terms_string")

        -------------------------------
        """
        
        self.validate_taxonomy_uid()
        self.validate_term_string(term_string)
        Parameter.add_param(self, "term", term_string)
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
    def move(self, data: dict, terms_uid: str = None):
        """
        The "Move terms" call will let you update the details
        
        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It will be converted to a JSON string before sending the request
        :type data: dict
        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        the terms you want to move
        :type terms_uid: str
        :return: Json, with updated taxonomy details.
        -------------------------------
        [Example:]
            >>> data ={
            >>>        "term": {
            >>>            "uid": "term_1"
            >>>        },
            >>>        "parent_uid": null
            >>>        }
            >>>        Under an existing Term:
            >>>        {
            >>>        "term": {
            >>>            "uid": "term_3"
            >>>        },
            >>>        "parent_uid": "term_1"
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy("taxonomy_uid").terms('terms_uid').move(data).json()

        -------------------------------
        """
        
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid

        self.validate_taxonomy_uid()
        self.validate_terms_uid()
        url = f"{self.path}/{self.terms_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    

    def ancestors(self, terms_uid: str = None):
        """
         The "Get a ancestors terms" call returns information about a specific terms available on the taxonomy.

        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        a term in a taxonomy. It is used to specify the term for which you want to retrieve the
        ancestors
        :type terms_uid: str
        :return: The code is returning the result of a GET request to the specified URL, which is the
        ancestors of the terms with the given terms_uid.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').terms('terms_uid').ancestors().json()

        -------------------------------
        """
        
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid
            
        self.validate_taxonomy_uid()
        self.validate_terms_uid()
        url = f"{self.path}/{self.terms_uid}/ancestors"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def descendants(self, terms_uid: str = None):
        """
        The "Get a descendants terms" call returns information about a specific terms available on the taxonomy.
        
        :param terms_uid: The `terms_uid` parameter is a string that represents the unique identifier of
        a term in a taxonomy. It is used to specify the term for which you want to retrieve its
        descendants
        :type terms_uid: str
        :return: the result of a GET request to the specified URL.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').taxonomy('taxonomy_uid').terms('terms_uid').descendants().json()

        -------------------------------
        """
        
        if terms_uid is not None and terms_uid != '':
            self.terms_uid = terms_uid
            
        self.validate_taxonomy_uid()
        self.validate_terms_uid()
        url = f"{self.path}/{self.terms_uid}/descendants"
        return self.client.get(url, headers = self.client.headers, params = self.params)
      
    def validate_taxonomy_uid(self):
        if self.taxonomy_uid is None or '':
            raise ArgumentException('Taxonomy Uid is required')
    
    def validate_terms_uid(self):
        if self.terms_uid is None or '':
            raise ArgumentException('Terms Uid is required')
        
    def validate_term_string(self, term_string):
        if term_string is None or '':
            raise ArgumentException('Term String is required')
        
    
    