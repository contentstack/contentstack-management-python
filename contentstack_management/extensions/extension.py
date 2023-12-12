"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException
from requests_toolbelt.multipart.encoder import MultipartEncoder

class Extension(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, extension_uid: str):
        self.client = client
        self.extension_uid = extension_uid
        super().__init__(self.client)

        self.path = "extensions"

    def find(self):
        """
        The "Get all custom fields" request is used to get the information of all custom fields created in a stack.
        :return: Json, with extension details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").extension().find().json()
        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The "Fetch" request returns information about a specific extension.
        :return: Json, with extension details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').extension('extension_uid').fetch().json()
        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.extension_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def upload(self, data: dict):
        """
        The Upload is used to upload a new custom widget, custom field, dashboard Widget to a stack.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with extension details.
        -------------------------------
        [Example:]
            >>> extension = {
            >>>        "file_name": "demo.html",
            >>>        "file_path": "/Users/sunil.lakshman/Downloads/demo.html",
            >>>        "data_type": 'text',
            >>>        "title": 'Old Extension',
            >>>        "multiple": False,
            >>>        "tags": {},
            >>>        "type": 'dashboard'
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').extension().upload(extension).json()
        -------------------------------
        """

        fields = {
            'extension[upload]': (f"{data['file_name']}", open(f"{data['file_name']}", 'rb'), 'text/html'),
            'extension[title]': f"{data['title']}",
            'extension[data_type]': f"{data['data_type']}",
            'extension[type]': f"{data['type']}",
            'extension[tags]': f"{data['tags']}",
            'extension[multiple]': f"{data['multiple']}"
        }
        content_type, body = self.encode_multipart_formdata(fields)
        self.client.headers['Content-Type'] = content_type
        return self.client.post(self.path, headers = self.client.headers, data = body, params = self.params)
    
    def create(self, data: dict):
        """
        The Create a extension call creates a new extension in a particular stack of your Contentstack account.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated extension details.
        -------------------------------
        [Example:]
            >>> extension = {
            >>>            tags: [
            >>>            'tag1',
            >>>            'tag2'
            >>>            ],
            >>>            data_type: 'text',
            >>>            title: 'Old Extension',
            >>>            src: "Enter either the source code (use 'srcdoc') or the external hosting link of the extension depending on the hosting method you selected.",
            >>>            multiple: false,
            >>>            config: {},
            >>>            type: 'field'
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').extension("extension_uid").update(extension).json()
        -------------------------------
        """
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The "Update Extensions call" will update the details of a custom field.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated extension details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "extension": {
            >>>            "tags": [
            >>>                "tag1",
            >>>                "tag2"
            >>>            ],
            >>>            "data_type": "text",
            >>>            "title": "Old Extension",
            >>>            "src": "Enter either the source code (use 'srcdoc') or the external hosting link of the extension depending on the hosting method you selected.",
            >>>            "multiple": false,
            >>>            "config": "{}",
            >>>            "type": "field"
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').extension("extension_uid").update(data).json()
        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.extension_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The "Delete custom field" request deletes a specific custom field.

        :return: The delete() method returns the status code and message as a response.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').extension('extension_uid').delete().json()
        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.extension_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def validate_uid(self):
         if self.extension_uid is None or '':
            raise ArgumentException("Extension Uid is required")
         
    def encode_multipart_formdata(self, fields):
        # Create a MultipartEncoder instance with the specified fields
        encoder = MultipartEncoder(fields)
        # Set the content type to the encoder's content type
        content_type = encoder.content_type
        # Get the encoded body
        body = encoder.to_string()
        return content_type, body