"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Auditlog(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, log_item_uid: str):
        self.client = client
        self.log_item_uid = log_item_uid
        super().__init__(self.client)

        self.path = "audit-logs"

    def find(self):
        """
       The "Get audit log" request is used to retrieve the audit log of a stack.
        :return: Json, with auditlog details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").auditlog().find().json()

        -------------------------------
        """  
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The "Get audit log item" request is used to retrieve a specific item from the audit log of a stack.
        :return: Json, with auditlog details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').auditlog('log_item_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.log_item_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def validate_uid(self):
        if self.log_item_uid is None or '':
            raise ArgumentException('Log item Uid is required')
        
    