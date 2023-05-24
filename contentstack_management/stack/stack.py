"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from json import JSONDecodeError
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
import contentstack_management



class Stack:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, api_key):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.api_key = api_key

    def fetch(self):
        url = "stacks"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    


