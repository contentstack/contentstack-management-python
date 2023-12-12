"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class Locale(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, locale_code: str):
        self.client = client
        self.locale_code = locale_code
        super().__init__(self.client)

        self.path = "locales"

    def find(self):
        """
        This call fetches the list of all languages (along with the language codes) available for a stack.
        :return: Json, with locale details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").locale().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The "Get a language" call returns information about a specific language available on the stack.
        :return: Json, with locale details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').locale('locale_code').fetch().json()

        -------------------------------
        """
        self.validate_locale_code()
        url = f"{self.path}/{self.locale_code}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data: dict):
        """
        This call lets you add a new language to your stack. You can either add a supported language or a custom language of your choice.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with locale details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "locale":{
            >>>            "name":"Arabic - Bahrain",
            >>>            "code":"ar-bh",
            >>>            "fallback_locale":"en-us"
            >>>         }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').locale().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data: dict):
        """
        The "Update language" call will let you update the details (such as display name)
          and the fallback language of an existing language of your stack.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated locale details.
        -------------------------------
        [Example:]
            >>> data ={
            >>>        "locale":{
            >>>            "name":"Updated Locale Name",
            >>>            "fallback_locale":"zh-cn"
            >>>         }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').locale("locale_code").update(data).json()

        -------------------------------
        """
        
        self.validate_locale_code()
        url = f"{self.path}/{self.locale_code}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The "Delete language" call deletes an existing language from your stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = result = client.stack('api_key').locale('locale_code').delete().json()

        -------------------------------
        """
        
        
        self.validate_locale_code()
        url = f"{self.path}/{self.locale_code}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def set_fallback(self, data: dict):
        """
        The "Set a fallback" language request allows you to assign a fallback language for an entry in a particular language.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with locale details.

        -------------------------------
        [Example:]
            >>> data ={
            >>>        "locale":{
            >>>            "name":"Arabic - Bahrain",
            >>>            "code":"ar-bh",
            >>>            "fallback_locale":"en-us"
            >>>         }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').locale().set_fallback(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update_fallback(self, data: dict):
        """
        The "Update fallback language" request allows you to update the fallback language for an existing language of your stack.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated locale details.
        -------------------------------
        [Example:]
            >>> data ={
            >>>        "locale":{
            >>>            "name":"Updated Locale Name",
            >>>            "fallback_locale":"zh-cn"
            >>>         }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').locale('locale_code').update_fallback(data).json()

        -------------------------------
        """
        
        self.validate_locale_code()
        url = f"{self.path}/{self.locale_code}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
        
    def validate_locale_code(self):
        if self.locale_code is None or '':
            raise ArgumentException('Locale code is required')
        
    
    