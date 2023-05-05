
import json
from json import JSONDecodeError
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
import contentstack_cms

class Error:

    def __init__(self, data):
        self.data = data
        self.err_message = data["error_message"]
        self.err_code = data["error_code"]
        self.error_detail = data["error_detail"]
        print("initialise the error class")

    @property
    def error(self):
    
        self.err_message = self.data["error_message"]
        self.err_code = self.data["error_code"]
        return self.data

    @property
    def error_message(self):
     
        return self.err_message

    @property
    def error_code(self):
 
        return self.err_code

    @property
    def error_detail(self):
    
        return self.error_detail

    @error_detail.setter
    def error_detail(self, value):
        self._error_detail = value
