"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The query(), create(), fetch(), delete(), update(), versions(), and includeVariants() methods each correspond to 
the operations that can be performed on the API """

import json
from ..common import Parameter
from .._errors import ArgumentException
from .._messages import ENTRY_VARIANT_CONTENT_TYPE_UID_REQUIRED, ENTRY_VARIANT_ENTRY_UID_REQUIRED, ENTRY_VARIANT_UID_REQUIRED

class EntryVariants(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The query(), create(), fetch(), delete(), update(), versions(), and includeVariants() 
    methods each correspond to the operations that can be performed on the API """

    def __init__(self, client, content_type_uid: str, entry_uid: str, variant_uid: str = None):
        self.client = client
        self.content_type_uid = content_type_uid
        self.entry_uid = entry_uid
        self.variant_uid = variant_uid
        super().__init__(self.client)
        self.path = f"content_types/{content_type_uid}/entries/{entry_uid}/variants"


    def find(self, params: dict = None):
        """
        The Find variant entries call fetches all the existing variant customizations for an entry.
        
        :param params: The `params` parameter is a dictionary that contains query parameters to be sent with the request
        :type params: dict
        :return: Json, with variant entry details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").content_types('content_type_uid').entry('entry_uid').variants().query().find().json()
            >>> # With parameters
            >>> result = client.stack("api_key").content_types('content_type_uid').entry('entry_uid').variants().find({'limit': 10, 'skip': 0}).json()

        -------------------------------
        """        
        self.validate_content_type_uid()
        self.validate_entry_uid()
        if params is not None:
            self.params.update(params)
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
    def create(self, data: dict):
        """
        This call is used to create a variant entry for an entry.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with variant entry details.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "customized_fields": [
            >>>            "title",
            >>>            "url"
            >>>        ],
            >>>        "base_entry_version": 10,  # optional
            >>>        "entry": {
            >>>            "title": "example",
            >>>            "url": "/example"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants().create(data).json()

        -------------------------------
        """
        self.validate_content_type_uid()
        self.validate_entry_uid()
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def fetch(self, variant_uid: str = None, params: dict = None):
        """
        The fetch Variant entry call fetches variant entry details.
        
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        a variant. It is used to specify which variant to fetch from the server
        :type variant_uid: str
        :param params: The `params` parameter is a dictionary that contains query parameters to be sent with the request
        :type params: dict
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').fetch().json()
            >>> # With parameters
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').fetch(params={'include_count': True}).json()

        -------------------------------
        """
        
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid

        self.validate_content_type_uid()
        self.validate_entry_uid()
        self.validate_variant_uid()
        if params is not None:
            self.params.update(params)
        url = f"{self.path}/{self.variant_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def delete(self, variant_uid: str = None): 
        """
        The delete a variant entry call is used to delete a specific variant entry.
        
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        the variant that you want to delete
        :type variant_uid: str
        :return: the result of the `client.delete()` method, which is likely a response object or a
        boolean value indicating the success of the deletion operation.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').delete().json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        self.validate_content_type_uid()
        self.validate_entry_uid()
        self.validate_variant_uid()
        url = f"{self.path}/{self.variant_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def update(self, data: dict, variant_uid: str = None):
        """
        The update a variant entry call updates an entry of a selected variant entry.
        
        :param data: The `data` parameter is a dictionary that contains the updated information that you
        want to send to the server. This data will be converted to a JSON string before sending it in
        the request
        :type data: dict
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        the variant. It is used to specify which variant should be updated with the provided data
        :type variant_uid: str
        :return: the result of the `put` request made to the specified URL.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "customized_fields": [
            >>>            "title",
            >>>            "url"
            >>>        ],
            >>>        "base_entry_version": 10,  # optional
            >>>        "entry": {
            >>>            "title": "example",
            >>>            "url": "/example"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').update(data).json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        self.validate_content_type_uid()
        self.validate_entry_uid()
        self.validate_variant_uid()
        url = f"{self.path}/{self.variant_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    def versions(self, variant_uid: str = None, params: dict = None):
        """
        The version method retrieves the details of a specific variant entry version details.
        
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        the variant. It is used to specify which variant to get versions for
        :type variant_uid: str
        :param params: The `params` parameter is a dictionary that contains query parameters to be sent with the request
        :type params: dict
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').versions().json()
            >>> # With parameters
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').variants('variant_uid').versions(params={'limit': 10}).json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        self.validate_content_type_uid()
        self.validate_entry_uid()
        self.validate_variant_uid()
        if params is not None:
            self.params.update(params)
        url = f"{self.path}/{self.variant_uid}/versions"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def includeVariants(self, include_variants: str = 'true', variant_uid: str = None, params: dict = None):
        """
        The includeVariants method retrieves the details of a specific base entry with variant details.
        
        :param include_variants: The `include_variants` parameter is a string that specifies whether to include variants
        :type include_variants: str
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        the variant. It is used to specify which variant to include
        :type variant_uid: str
        :param params: The `params` parameter is a dictionary that contains query parameters to be sent with the request
        :type params: dict
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').includeVariants('true', 'variant_uid').json()
            >>> # With parameters
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').includeVariants('true', 'variant_uid', params={'locale': 'en-us'}).json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        self.validate_content_type_uid()
        self.validate_entry_uid()
        self.validate_variant_uid()
        if params is not None:
            self.params.update(params)
        self.params['include_variants'] = include_variants
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def validate_content_type_uid(self):
        """
        The function checks if the content_type_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.content_type_uid is None or self.content_type_uid == '':
            raise ArgumentException(ENTRY_VARIANT_CONTENT_TYPE_UID_REQUIRED)
    
    def validate_entry_uid(self):
        """
        The function checks if the entry_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.entry_uid is None or self.entry_uid == '':
            raise ArgumentException(ENTRY_VARIANT_ENTRY_UID_REQUIRED)
    
    def validate_variant_uid(self):
        """
        The function checks if the variant_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.variant_uid is None or self.variant_uid == '':
            raise ArgumentException(ENTRY_VARIANT_UID_REQUIRED)
