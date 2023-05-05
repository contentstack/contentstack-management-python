"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from json import JSONDecodeError
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
import contentstack_cms
from contentstack_cms.core.http_client import HttpClient




class Stacks:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.obj = HttpClient()


    def fetch(self):
        response = self.obj.read_api(self.url, self.headers)
        return response

