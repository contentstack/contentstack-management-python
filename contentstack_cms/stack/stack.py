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




class Stack:
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


    def content_type(self, content_type_uid=None):
        response = ContentType(content_type_uid)
        return response

