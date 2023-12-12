"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Metadata(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, metadata_uid: str):
        self.client = client
        self.metadata_uid = metadata_uid
        super().__init__(self.client)

        self.path = "metadata"

    def find(self):
        """
        The Get All Metadata request returns comprehensive information of all the metadata attached to all the entries and assets in your stack.
        :return: Json, with Metadata details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").metadata().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Get metadata request fetches the metadata attached to a specific asset or entry of a stack.
        :return: Json, with Metadata details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata('metadata_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.metadata_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Create metadata request lets you create metadata for a specific asset or entry. 
        Whenever you create metadata for an entry or asset, you need to specify the extension to which it will be connected.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with Metadata details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "metadata": {
            >>>            "entity_uid": "entity_uid",
            >>>            "type": "entry",
            >>>            "_content_type_uid": "sample_content",
            >>>            "extension_uid": "extension_uid",
            >>>            "presets": [{
            >>>                "uid": "presents_uid",
            >>>                "name": "Test1",
            >>>                "options": {
            >>>                }
            >>>            }]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The Update metadata request lets you update the metadata for a specific entry or asset.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated Metadata details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "metadata": {
            >>>            "entity_uid": "entity_uid",
            >>>            "type": "entry",
            >>>            "extension_uid": "extension_uid",
            >>>            "locale": "en_us",
            >>>            "_content_type_uid": "_content_type_uid",
            >>>            "presets": [{
            >>>                    "uid": "presets_uid",
            >>>                    "name": "test1",
            >>>                    "options": {}
            >>>                },
            >>>                {
            >>>                    "name": "Test3",
            >>>                    "uid": "presets_uid",
            >>>                    "options": {
            >>>                        "quality": "100",
            >>>                        "transform": {
            >>>                            "height": 500,
            >>>                            "width": 500
            >>>                        },
            >>>                        "image-type": "jpeg",
            >>>                        "focal-point": {
            >>>                            "x": 0,
            >>>                            "y": 0
            >>>                        }
            >>>                    }
            >>>                }
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata("metadata_uid").update(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.metadata_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete metadata request lets you delete the metadata associated with a specific entry or asset.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata('metadata_uid').delete().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.metadata_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def publish(self, data: dict):
        """
        The Publish metadata request lets you publish the metadata associated with a specific entry or asset.
        
        :return: Json, with updated Metadata details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "metadata": {
            >>>            "environments": [
            >>>            "test"
            >>>            ],
            >>>            "locales": [
            >>>            "en-us"
            >>>            ]
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata('metadata_uid').publish(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.metadata_uid}/publish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    def unpublish(self, data: dict):
        """
        The Unpublish metadata request lets you unpublish the metadata associated with a specific entry or asset.
        :return: Json, with updated Metadata details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "metadata": {
            >>>            "environments": [
            >>>            "test"
            >>>            ],
            >>>            "locales": [
            >>>            "en-us"
            >>>            ]
            >>>        }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').metadata('metadata_uid').unpublish(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.metadata_uid}/unpublish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    def validate_uid(self):
         if self.metadata_uid is None or '':
            raise ArgumentException("Metadata Uid is required")