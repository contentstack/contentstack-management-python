"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class ReleaseItems(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, release_uid: str):
        self.client = client
        self.release_uid = release_uid
        super().__init__(self.client)
        self.path = f"releases/{self.release_uid}"

    def find(self):
        """
        The "Get all items in a Release request" retrieves a list of all items (entries and assets) that are part of a specific Release.
        :return: Json, with releases details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").releases("release_uid").item().find()

        -------------------------------
        """     
        url = f"{self.path}/items"  
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The "Add a single item to a Release" request allows you to add an item (entry or asset) to a Release.
        
        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It will be converted to a JSON string using the `json.dumps()` function before
        being sent in the request
        :type data: dict
        :return: The code is returning the result of the `post` method call on the `self.client` object.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "item": {
            >>>            "version": 1,
            >>>            "uid": "entry_or_asset_uid",
            >>>            "content_type_uid": "your_content_type_uid",
            >>>            "action": "publish",
            >>>            "locale": "en-us"
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').item().create(data)
        -------------------------------
        """
        
        data = json.dumps(data)
        url = f"{self.path}/item"
        return self.client.post(url, headers = self.client.headers, data=data, params = self.params)
    
    def create_multiple(self, data: dict):
        """
        The "Add multiple items to a Release" request allows you to add multiple items (entries and/or assets) to a Release.

        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It will be converted to a JSON string using the `json.dumps()` function before
        being sent in the request
        :type data: dict
        :return: The code is returning the result of the `post` method call on the `self.client` object.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "items": [{
            >>>            "uid": "entry_or_asset_uid1",
            >>>            "version": 1,
            >>>            "locale": "en-us",
            >>>            "content_type_uid": "demo1",
            >>>            "action": "publish"
            >>>        }, {
            >>>            "uid": "entry_or_asset_uid2",
            >>>            "version": 4,
            >>>            "locale": "fr-fr",
            >>>            "content_type_uid": "demo2",
            >>>            "action": "publish"
            >>>        }]
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').item().create_multiple(data)
        -------------------------------
        """
        
        data = json.dumps(data)
        url = f"{self.path}/items"
        return self.client.post(url, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The "Update Release items to their latest versions" request let you update all the release items (entries and assets) to their latest versions before deployment
        
        :param data: A dictionary containing the data to be updated
        :type data: dict
        :param item_uid: The `item_uid` parameter is a string that represents the unique identifier of
        the item you want to update
        :type item_uid: str
        :return: the result of the `self.client.put()` method, which is the response from making a PUT
        request to the specified URL with the provided data and headers.

        -------------------------------
        [Example:]
            >>> data ={
            >>>    "items":[
            >>>        "$all"
            >>>    ]
            >>>  }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases("release_uid").item().update(data)

        -------------------------------
        """

        self.validate_release_uid()
        url = f"{self.path}/update_items"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self,  data: dict): 
        """
        The "Remove an item from a Release" request removes one or more items (entries and/or assets) from a specific Release.
        
        :param item_uid: The `item_uid` parameter is a string that represents the unique identifier of
        the item you want to delete
        :type item_uid: str
        :return: the result of the delete request made to the specified URL.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "items": [{
            >>>            "uid": "items_uid",
            >>>            "version": 1,
            >>>            "locale": "ja-jp",
            >>>            "content_type_uid": "category",
            >>>            "action": "publish"
            >>>        }]
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').releases('release_uid').item().delete(data)

        -------------------------------
        """
         
        self.validate_release_uid()
        url = f"{self.path}/items"
        data = json.dumps(data)
        return self.client.delete(url, headers = self.client.headers, data=data, params = self.params)
    
    def delete_multiple(self,  data: dict):
        """
        The "Remove an item from a Release" request removes one or more items (entries and/or assets) from a specific Release.
        
        :param item_uid: The `item_uid` parameter is a string that represents the unique identifier of
        the item you want to delete
        :type item_uid: str
        :return: the result of the delete request made to the specified URL.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "items": [{
            >>>            "uid": "item_uid",
            >>>            "locale": "en-us",
            >>>            "version": 1,
            >>>            "content_type_uid": "your_content_type_uid",
            >>>            "action": "publish_or_unpublish"
            >>>        }]
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').releases('release_uid').item().delete_multiple(data)

        -------------------------------
        """
        self.validate_release_uid()
        url = f"{self.path}/items"
        self.add_param("all", True)
        data = json.dumps(data)
        return self.client.delete(url, headers = self.client.headers, data=data, params = self.params)
    
    def validate_release_uid(self):
        if self.release_uid is None or '':
            raise ArgumentException('Releases Uid is required')
    
        
        
    
    