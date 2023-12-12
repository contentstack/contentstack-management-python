"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter

class Entry(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, content_type_uid, entry_uid):
        self.client = client
        self.content_type_uid = content_type_uid
        self.entry_uid = entry_uid
        super().__init__(self.client)

        self.path = f"content_types/{content_type_uid}/entries/"

    def find(self):
        """
        The Get all entries call fetches the list of all the entries of a particular content type. 
        It also returns the content of each entry in JSON format. You can also specify the environment and locale of which you wish to get the entries.
        :return: the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack("api_key").content_types('content_type_uid').entry().find().json()

        -------------------------------
        """
        
        url = f"content_types/{self.content_type_uid}/entries"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Get a single entry request fetches a particular entry of a content type.
        :return: the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').fetch().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data, locale='en-us'):
        """
        The Create an entry call creates a new entry for the selected content type.
        
        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It represents the content of the entry that you want to create. The structure and
        content of this dictionary will depend on the specific requirements of your application and the
        content type of the entry you are creating
        :param locale: The `locale` parameter is used to specify the language and region for the content
        being created. It is set to `'en-us'` by default, which represents English language content for
        the United States. However, you can pass a different locale value to create content in a
        different language or region, defaults to en-us (optional)
        :return: the result of the response object.
        -------------------------------
        [Example:]
            >>> data = {
            >>>          "entry": {
            >>>                     "title": "example",
            >>>                     "url": "/example"
            >>>                  }
            >>>         }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types().entry().create(data).json()

        -------------------------------
        """

        url = f"content_types/{self.content_type_uid}/entries"
        self.params['locale'] = locale
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, params = self.params, data=data)
    
    def update(self, data, locale='en-us'):
        """
        The Update an entry call lets you update the content of an existing entry.
        
        :param data: The `data` parameter is the updated data that you want to send to the server. It
        should be a dictionary containing the fields and their updated values for the entry
        :param locale: The `locale` parameter is used to specify the language and region for the
        content. It is set to `'en-us'` by default, which represents English language content for the
        United States. You can change the value of `locale` to the desired language and region code to
        update the content in, defaults to en-us (optional)
        :return: the result of the response object.
        -------------------------------
        [Example:]
            >>> 
            >>> data = {
            >>>           "entry": {
            >>>                    "title": "example",
            >>>                    "url": "/example"
            >>>            }
            >>>         }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').update(data).json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}"
        self.params['locale'] = locale
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, params = self.params, data=data)
    
    
    def version_naming(self, version_number, data):
        """
        The Set Version Name for Entry request allows you to assign a name to a specific version of an entry.
        
        :param version_number: The version number is the identifier for a specific version of an entry.
        It is used to differentiate between different versions of the same entry
        :param data: The `data` parameter is a dictionary that contains the information you want to send
        in the request body. It will be converted to a JSON string using the `json.dumps()` function
        before sending the request
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> data ={
            >>>                "entry": {
            >>>                    "_version_name": "Test version",
            >>>                    "locale": "en-us",
            >>>                    "force": true
            >>>                }
            >>>            }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').version_naming(data).json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        if version_number is None:
            raise Exception('Version Number is required')
        if data is None:
            raise Exception('Body is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/versions/{version_number}/name"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers,  data=data, params = self.params)
    
    def references(self):
        """
        The Get references of an entry call returns all the entries of content types that are referenced by a particular entry.
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').references().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/references"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def languages(self):
        """
       The Get languages of an entry call returns the details of all the languages that an entry exists in.
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').languages().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/locales"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def localize(self, data, locale='en-us'):
        """
        The Localize an entry request allows you to localize an entry i.e., 
        the entry will cease to fetch data from its fallback language and possess independent content specific to the selected locale.
        
        :param data: The `data` parameter is the content that you want to localize. It should be a
        dictionary or JSON object containing the fields and values that you want to update or add for
        the specified locale
        :param locale: The `locale` parameter is used to specify the language and region for
        localization. It is set to `'en-us'` by default, which represents English (United States). You
        can change the value of `locale` to any supported language and region code according to your
        requirements, defaults to en-us (optional)
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> data ={
            >>>               "entry": {
            >>>                   "title": "Home",
            >>>                    "url": "/home-french",
            >>>                    "tags": [],
            >>>                    "locale": "en-us",
            >>>                    "uid": "entry_uid",
            >>>                    "created_by": "user_uid",
            >>>                    "updated_by": "user_uid",
            >>>                    "created_at": "2017-06-13T12:34:52.083Z",
            >>>                    "updated_at": "2018-12-28T06:33:06.752Z",
            >>>                    "ACL": {},
            >>>                    "_version": 2
            >>>                    }
            >>>            }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').localize(data).json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        if data is None:
            raise Exception('Body is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}"
        self.params['locale'] = locale
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, params = self.params, data = data)
    
    def unlocalize(self, locale='en-us'):
        """
        The Unlocalize an entry request is used to unlocalize an existing entry. 
        
        :param locale: The `locale` parameter is a string that represents the locale or language code.
        It specifies the language in which the content should be unlocalized. The default value is
        'en-us', which stands for English (United States), defaults to en-us (optional)
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').unlocalize().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/unlocalize"
        self.params['locale'] = locale
        return self.client.post(url, headers = self.client.headers, params = self.params)
    
    
    def delete(self):
        """
        The Delete an entry request allows you to delete a specific entry from a content type. 
        This API request also allows you to delete single and/or multiple localized entries.
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = result = client.stack('api_key').content_types('content_type_uid').entry('entry_uid').delete().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}"
        self.params['force'] = True
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def imports(self, file_path, locale='en-us'):
        """
        The Import an entry call is used to import an entry. To import an entry, 
        you need to upload a JSON file that has entry data in the format that fits the schema of the content type it is being imported to.
        
        :param file_path: The file path is the path to the file that you want to import. It should be a
        string that specifies the location of the file on your computer
        :param locale: The `locale` parameter is used to specify the language and region for the
        imported content. It is set to `'en-us'` by default, which represents English (United States).
        You can change the value of `locale` to the desired language and region code according to your
        requirements, defaults to en-us (optional)
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> file_path = "tests/resources/mock_content_types/import_content_types.json"
            >>> result = client.stack('api_key').content_types().entry('entry_uid').imports(file_path).json()

        -------------------------------
        """
        if file_path is None:
            raise Exception('File path is required')
        url = f"content_types/{self.content_type_uid}/entries/import"
        self.client.headers['Content-Type'] = "multipart/form-data"
        files = {'entry': open(f"{file_path}",'rb')}
        self.params['locale'] = locale
        return self.client.post(url, headers = self.client.headers, params = self.params, files = files)
    
    def export(self):
        """
        The Export an entry call is used to export an entry. The exported entry data is saved in a downloadable JSON file.
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types().entry('entry_uid').export().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/export"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def publish(self, data):
        """
        The Publish an entry request lets you publish an entry either immediately or schedule it for a later date/time.
        
        :param data: The `data` parameter is a dictionary that contains the data to be published. It
        will be converted to a JSON string using the `json.dumps()` function before being sent in the
        request
        :return:  the result of the response object.
        -------------------------------
        [Example:]

            >>> data = {
            >>>                "entry": {
            >>>                    "environments": ["development"],
            >>>                    "locales": ["en-us"]
            >>>                },
            >>>                "locale": "en-us",
            >>>                "version": 1,
            >>>                "scheduled_at": "2019-02-14T18:30:00.000Z"
            >>>            }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types().entry('entry_uid').publish(data).json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        if data is None:
            raise Exception('Body is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/publish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    def unpublish(self, data):
        """
        The Unpublish an entry call will unpublish an entry at once, and also, 
        gives you the provision to unpublish an entry automatically at a later date/time.
        
        :param data: The `data` parameter is a JSON object that contains the necessary information for
        unpublishing a content type. It should include the content type UID (unique identifier) and any
        additional data required for the unpublishing process
        :return: the result of the response object.
        -------------------------------
        [Example:]

            >>> data = {
            >>>                "entry": {
            >>>                    "environments": ["development"],
            >>>                    "locales": ["en-us"]
            >>>                },
            >>>                "locale": "en-us",
            >>>                "version": 1,
            >>>                "scheduled_at": "2019-02-14T18:30:00.000Z"
            >>>            }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').content_types().entry('entry_uid').unpublish().json()

        -------------------------------
        """
        if self.entry_uid is None:
            raise Exception('Entry uid is required')
        if data is None:
            raise Exception('Body is required')
        url = f"content_types/{self.content_type_uid}/entries/{self.entry_uid}/unpublish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    
    
    
    

    

    


