"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException
from ..release_items.release_item import ReleaseItems

class Releases(Parameter):
    """
    You can define a “Release” as a set of entries and assets that needs to be deployed (published or unpublished) all at once to a particular environment.
    """

    def __init__(self, client, release_uid: str):
        self.client = client
        self.release_uid = release_uid
        super().__init__(self.client)
        self.path = "releases"

    def find(self):
        """
        The find request gets the details of all Releases in a stack.
        :return: Json, with releases details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").releases().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Fetch request gets the details of a specific Release in a stack.
        :return: Json, with releases details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.release_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        The Create request allows you to create a new Release in your stack. 
        To add entries/assets to a Release, you need to provide the UIDs of the entries/assets in `items` in the request body.
        
        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with releases details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "release": {
            >>>            "name": "Release Name",
            >>>            "description": "2018-12-12",
            >>>            "locked": false,
            >>>            "archived": false
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The Update call allows you to update the details of a Release, i.e., the `name` and `description`.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated releases details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "release": {
            >>>            "name": "Release Name",
            >>>            "description": "2018-12-22"
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases("release_uid").update(data).json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.release_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete request allows you to delete a specific Release from a stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').delete().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.release_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def deploy(self, data: dict):
        """
        You can pin a set of entries and assets (along with the deploy action,
        i.e., publish/unpublish) to a release, and then deploy this release to an environment.
        This will publish/unpublish all the items of the release to the specified environment.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with releases details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "release": {
            >>>            "environments": [
            >>>                "development"
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').deploy(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        url = f"{self.path}/{self.release_uid}/deploy"
        return self.client.post(url, headers = self.client.headers, data=data, params = self.params)
    
    def clone(self, data: dict):
        """
        The Clone request allows you to clone (make a copy of) a specific Release in a stack.
        
        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with releases details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "release": {
            >>>            "name": "New Release Name",
            >>>            "description": "2018-12-12"
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').releases('release_uid').clone(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        url = f"{self.path}/{self.release_uid}/clone"
        return self.client.post(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def validate_uid(self):
         if self.release_uid is None or '':
            raise ArgumentException("Releases Uid is required")
         
    def item(self):
            self.validate_uid()
            return ReleaseItems(self.client, self.release_uid)
    
         