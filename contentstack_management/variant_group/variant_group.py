"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from .._errors import ArgumentException
from ..variants.variants import Variants

class VariantGroup(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, variant_group_uid: str = None):
        self.client = client
        self.variant_group_uid = variant_group_uid
        super().__init__(self.client)
        self.path = "variant_groups"

    def find(self):
        """
        The Find variant group call fetches all the existing variant groups of the stack.
        :return: Json, with variant group details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").variant_group().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
    def query(self, query_params: dict = None):
        """
        The Query on variant group will allow to fetch details of all or specific variant groups with filtering.
        
        :param query_params: The `query_params` parameter is a dictionary that contains query parameters for filtering
        :type query_params: dict
        :return: Json, with filtered variant group details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").variant_group().query({'name': 'Colors'}).find().json()

        -------------------------------
        """
        if query_params is not None:
            self.params.update(query_params)
        return self
    
    def fetch(self, variant_group_uid: str = None):
        """
        The Get variant group call returns information about a particular variant group of a stack.
        
        :param variant_group_uid: The `variant_group_uid` parameter is a string that represents the unique identifier of
        a variant group. It is used to specify which variant group to fetch from the server
        :type variant_group_uid: str
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').variant_group('variant_group_uid').fetch().json()

        -------------------------------
        """
        
        if variant_group_uid is not None and variant_group_uid != '':
            self.variant_group_uid = variant_group_uid

        self.validate_uid()
        url = f"{self.path}/{self.variant_group_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    def create(self, data: dict):
        """
        This call is used to create a variant group.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with variant group details.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "name": "Colors",
            >>>        "content_types": [
            >>>            "iphone_product_page"
            >>>        ],
            >>>        "uid": "iphone_color_white"  # optional
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').variant_group().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict, variant_group_uid: str = None):
        """
        The "Update variant group" call is used to update an existing variant group.
        
        :param data: The `data` parameter is a dictionary that contains the updated information that you
        want to send to the server. This data will be converted to a JSON string before sending it in
        the request
        :type data: dict
        :param variant_group_uid: The `variant_group_uid` parameter is a string that represents the unique identifier of
        the variant group. It is used to specify which variant group should be updated with the provided data
        :type variant_group_uid: str
        :return: the result of the `put` request made to the specified URL.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "name": "iPhone Colors",
            >>>        "content_types": [
            >>>            {"uid": "iphone_product_page", "status": "linked"}
            >>>        ],
            >>>        "personalize_metadata": {
            >>>            "experience_uid": "variant_group_ex_uid_update",
            >>>            "experience_short_uid": "variant_group_short_uid_update",
            >>>            "project_uid": "variant_group_project_uid_update",
            >>>            "status": "linked"
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').variant_group("variant_group_uid").update(data).json()

        -------------------------------
        """
        if variant_group_uid is not None and variant_group_uid != '':
            self.variant_group_uid = variant_group_uid
        self.validate_uid()
        url = f"{self.path}/{self.variant_group_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    def delete(self, variant_group_uid: str = None): 
        """
        The "Delete variant group" call is used to delete a specific variant group.
        
        :param variant_group_uid: The `variant_group_uid` parameter is a string that represents the unique identifier of
        the variant group that you want to delete
        :type variant_group_uid: str
        :return: the result of the `client.delete()` method, which is likely a response object or a
        boolean value indicating the success of the deletion operation.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').variant_group('variant_group_uid').delete().json()

        -------------------------------
        """
        if variant_group_uid is not None and variant_group_uid != '':
            self.variant_group_uid = variant_group_uid
        self.validate_uid()
        url = f"{self.path}/{self.variant_group_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def link_contenttypes(self, data: dict, variant_group_uid: str = None):
        if variant_group_uid is not None and variant_group_uid != '':
            self.variant_group_uid = variant_group_uid
        self.validate_uid()
        url = f"{self.path}/{self.variant_group_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    def unlink_contenttypes(self, data: dict, variant_group_uid: str = None):
        if variant_group_uid is not None and variant_group_uid != '':
            self.variant_group_uid = variant_group_uid
        self.validate_uid()
        url = f"{self.path}/{self.variant_group_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    def variants(self, variant_uid: str = None):
        """
        Returns a Variants instance for managing variants within this variant group.
        
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        a variant. It is used to specify which variant to work with
        :type variant_uid: str
        :return: Variants instance for managing variants
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # Get all variants
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants().find().json()
            >>> # Get specific variant
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants('variant_uid').fetch().json()

        -------------------------------
        """
        return Variants(self.client, self.variant_group_uid, variant_uid)
    
    def validate_uid(self):
        """
        The function checks if the variant_group_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.variant_group_uid is None or self.variant_group_uid == '':
            raise ArgumentException("variant group Uid is required")