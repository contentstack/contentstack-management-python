"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Label(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, label_uid: str):
        self.client = client
        self.label_uid = label_uid
        super().__init__(self.client)

        self.path = "labels"

    def find(self):
        """
        The Find label call fetches all the existing labels of the stack.
        :return: Json, with label details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").label().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self, label_uid: str = None):
        """
        The Get label call returns information about a particular label of a stack.
        
        :param label_uid: The `label_uid` parameter is a string that represents the unique identifier of
        a label. It is used to specify which label to fetch from the server
        :type label_uid: str
        :return: the result of the GET request made to the specified URL.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').label('label_uid').fetch().json()

        -------------------------------
        """
        
        if label_uid is not None and label_uid != '':
            self.label_uid = label_uid

        self.validate_uid()
        url = f"{self.path}/{self.label_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        This call is used to create a label.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with label details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "label": {
            >>>            "name": "Test",
            >>>            "parent": [
            >>>            "label_uid"
            >>>            ],
            >>>            "content_types": [
            >>>            "content_type_uid"
            >>>            ]
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').label().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict, label_uid: str = None):
        """
        The "Update label" call is used to update an existing label.
        
        :param data: The `data` parameter is a dictionary that contains the updated information that you
        want to send to the server. This data will be converted to a JSON string before sending it in
        the request
        :type data: dict
        :param label_uid: The `label_uid` parameter is a string that represents the unique identifier of
        the label. It is used to specify which label should be updated with the provided data
        :type label_uid: str
        :return: the result of the `put` request made to the specified URL.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "label": {
            >>>            "name": "Test",
            >>>            "parent": [
            >>>            "label_uid"
            >>>            ],
            >>>            "content_types": [
            >>>            "content_type_uid"
            >>>            ]
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').label("label_uid").update(data).json()

        -------------------------------
        """
        if label_uid is not None and label_uid != '':
            self.label_uid = label_uid
        self.validate_uid()
        url = f"{self.path}/{self.label_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self, label_uid: str = None): 
        """
        The "Delete label" call is used to delete a specific label.
        
        :param label_uid: The `label_uid` parameter is a string that represents the unique identifier of
        the label that you want to delete
        :type label_uid: str
        :return: the result of the `client.delete()` method, which is likely a response object or a
        boolean value indicating the success of the deletion operation.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').label('label_uid').delete().json()

        -------------------------------
        """
        if label_uid is not None and label_uid != '':
            self.label_uid = label_uid
        self.validate_uid()
        url = f"{self.path}/{self.label_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def validate_uid(self):
        """
        The function checks if the label_uid is None or an empty string and raises an ArgumentException
        if it is.
        """
         
        if self.label_uid is None or '':
            raise ArgumentException("label Uid is required")