"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json

class Globalfields:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, global_field_uid):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.api_key = api_key
        self.global_field_uid = global_field_uid

    def fetch(self):
        """
        Fetches the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack("API_KEY").global_fields('global_field_uid').fetch().json()

        -------------------------------
        """
        url = f"global_fields/{self.global_field_uid}"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    
    def fetch_all(self):
        """
        Fetches the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').global_fields('global_field_uid').fetch_all().json()

        -------------------------------
        """
        url = "global_fields"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)
    
    def create(self, data):
        """
        Create the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]
            >>> data = {
                        "global_field": {
                            "title": "Servlet",
                            "uid": "servlet",
                            "schema": [{
                                "display_name": "Name",
                                "uid": "name",
                                "data_type": "text"
                            }, {
                                "data_type": "text",
                                "display_name": "Rich text editor",
                                "uid": "description",
                                "field_metadata": {
                                    "allow_rich_text": true,
                                    "description": "",
                                    "multiline": false,
                                    "rich_text_type": "advanced",
                                    "options": [],
                                    "version": 3
                                },
                                "multiple": false,
                                "mandatory": false,
                                "unique": false
                            }]
                        }
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').global_fields().create(data).json()

        -------------------------------
        """
        url = "global_fields"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data=data)
    
    def update(self, data):
        """
        Update the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]
            >>> data = {
                        "global_field": {
                            "title": "Servlet",
                            "uid": "servlet",
                            "schema": [{
                                "display_name": "Name",
                                "uid": "name",
                                "data_type": "text"
                            }, {
                                "data_type": "text",
                                "display_name": "Rich text editor",
                                "uid": "description",
                                "field_metadata": {
                                    "allow_rich_text": true,
                                    "description": "",
                                    "multiline": false,
                                    "rich_text_type": "advanced",
                                    "options": [],
                                    "version": 3
                                },
                                "multiple": false,
                                "mandatory": false,
                                "unique": false
                            }]
                        }
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').global_fields('global_field_uid').update(data).json()

        -------------------------------
        """
        url = f"global_fields/{self.global_field_uid}"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.put(url, headers = self.headers, data=data)
    
    def delete(self):
        """
        Delete the global fields  
        :return: Json, with status code and message.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = result = client.stack('API_KEY').global_fields('global_field_uid').delete().json()

        -------------------------------
        """
        url = f"global_fields/{self.global_field_uid}"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        params = {'force': True}
        return self.api_client.delete(url, headers = self.headers, params = params)
    
    def import_global_fields(self, file_path):
        """
        Import the global fields
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> file_path = "tests/resources/mock_global_fields/import_global_fields.json"
            >>> result = client.stack('API_KEY').global_fields().import_global_fields(file_path).json()

        -------------------------------
        """
        url = f"global_fields/import"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        self.headers['Content-Type'] = "multipart/form-data"
        params = {'include_branch': False}
        files = {'global_field': open(f"{file_path}",'rb')}
        return self.api_client.post(url, headers = self.headers, params = params, files = files)
    
    def export(self):
        """
        Export the global fields 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').global_fields().export().json()

        -------------------------------
        """
        url = f"global_fields/{self.global_field_uid}/export"
        self.headers['authtoken'] = self.authtoken
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers = self.headers)
    
    
    
    
    

    

    


