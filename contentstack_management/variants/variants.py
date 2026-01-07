"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from .._errors import ArgumentException
from .._messages import VARIANT_UIDS_NON_EMPTY_LIST_REQUIRED, VARIANT_GROUP_UID_REQUIRED, VARIANT_UID_REQUIRED

class Variants(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, variant_group_uid: str = None, variant_uid: str = None):
        self.client = client
        self.variant_group_uid = variant_group_uid
        self.variant_uid = variant_uid
        super().__init__(self.client)
        if self.variant_group_uid:
            self.path = f"variant_groups/{self.variant_group_uid}/variants"
        else:
            self.path = "variants"

    def find(self, params: dict = None):
        """
        The Find variants call fetches all the existing variants of a variant group or ungrouped variants.
        
        :param params: The `params` parameter is a dictionary that contains query parameters to be sent with the request
        :type params: dict
        :return: Json, with variant details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants
            >>> result = client.stack("api_key").variant_group('variant_group_uid').variants().find().json()
            >>> # For ungrouped variants
            >>> result = client.stack("api_key").variants().find().json()
            >>> # With parameters
            >>> result = client.stack("api_key").variants().find({'limit': 10, 'skip': 0}).json()

        -------------------------------
        """        
        if self.variant_group_uid:
            self.validate_variant_group_uid()
        if params is not None:
            self.params.update(params)
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
    def query(self, query_params: dict = None):
        """
        The Query on variants will allow to fetch details of all or specific variants with filtering.
        
        :param query_params: The `query_params` parameter is a dictionary that contains query parameters for filtering
        :type query_params: dict
        :return: Json, with filtered variant details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants with query
            >>> result = client.stack("api_key").variant_group('variant_group_uid').variants().query({'title': 'variant title'}).find().json()
            >>> # For ungrouped variants with query
            >>> result = client.stack("api_key").variants().query({'title': 'variant title'}).find().json()

        -------------------------------
        """
        if query_params is not None:
            self.params.update(query_params)
        return self
    
    def fetch(self, variant_uid: str = None, params: dict = None):
        """
        The Get variant call returns information about a particular variant of a variant group or ungrouped variant.
        
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
            >>> # For grouped variants
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants('variant_uid').fetch().json()
            >>> # For ungrouped variants
            >>> result = client.stack('api_key').variants('variant_uid').fetch().json()
            >>> # With parameters
            >>> result = client.stack('api_key').variants('variant_uid').fetch(params={'include_count': True}).json()

        -------------------------------
        """
        
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid

        if self.variant_group_uid:
            self.validate_variant_group_uid()
        self.validate_variant_uid()
        if params is not None:
            self.params.update(params)
        url = f"{self.path}/{self.variant_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    def create(self, data: dict):
        """
        This call is used to create a variant within a variant group or as an ungrouped variant.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with variant details.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "uid": "iphone_color_white",  # optional
            >>>        "name": "White"
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants().create(data).json()
            >>> # For ungrouped variants
            >>> result = client.stack('api_key').variants().create(data).json()

        -------------------------------
        """
        if self.variant_group_uid:
            self.validate_variant_group_uid()
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict, variant_uid: str = None):
        """
        The "Update variant" call is used to update an existing variant.
        
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
            >>>        "name": "updated name"
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants
            >>> result = client.stack('api_key').variant_group("variant_group_uid").variants('variant_uid').update(data).json()
            >>> # For ungrouped variants
            >>> result = client.stack('api_key').variants('variant_uid').update(data).json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        if self.variant_group_uid:
            self.validate_variant_group_uid()
        self.validate_variant_uid()
        url = f"{self.path}/{self.variant_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    def delete(self, variant_uid: str = None): 
        """
        The "Delete variant" call is used to delete a specific variant.
        
        :param variant_uid: The `variant_uid` parameter is a string that represents the unique identifier of
        the variant that you want to delete
        :type variant_uid: str
        :return: the result of the `client.delete()` method, which is likely a response object or a
        boolean value indicating the success of the deletion operation.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants('variant_uid').delete().json()
            >>> # For ungrouped variants
            >>> result = client.stack('api_key').variants('variant_uid').delete().json()

        -------------------------------
        """
        if variant_uid is not None and variant_uid != '':
            self.variant_uid = variant_uid
        if self.variant_group_uid:
            self.validate_variant_group_uid()
        self.validate_variant_uid()
        url = f"{self.path}/{self.variant_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def fetchByUIDs(self, variant_uids: list):
        """
        The fetchByUIDs on variant will allow to fetch specific variants by their UIDs.
        
        :param variant_uids: The `variant_uids` parameter is a list of strings that represents the unique identifiers of
        the variants that you want to fetch
        :type variant_uids: list
        :return: Json, with variant details for the specified UIDs.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> # For grouped variants
            >>> result = client.stack('api_key').variant_group('variant_group_uid').variants().fetchByUIDs(['uid1', 'uid2']).json()
            >>> # For ungrouped variants
            >>> result = client.stack('api_key').variants().fetchByUIDs(['uid1', 'uid2']).json()

        -------------------------------
        """
        if not isinstance(variant_uids, list) or len(variant_uids) == 0:
            raise ArgumentException(VARIANT_UIDS_NON_EMPTY_LIST_REQUIRED)
        
        if self.variant_group_uid:
            self.validate_variant_group_uid()
        
        # Convert list to comma-separated string
        uids_param = ','.join(variant_uids)
        params = self.params.copy()
        params['uid'] = uids_param
        
        return self.client.get(self.path, headers = self.client.headers, params = params)
    
    def validate_variant_group_uid(self):
        """
        The function checks if the variant_group_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.variant_group_uid is None or self.variant_group_uid == '':
            raise ArgumentException(VARIANT_GROUP_UID_REQUIRED)
    
    def validate_variant_uid(self):
        """
        The function checks if the variant_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.variant_uid is None or self.variant_uid == '':
            raise ArgumentException(VARIANT_UID_REQUIRED)