"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json

from contentstack_management.common import Parameter

_path = 'global_fields'


class GlobalFields(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, global_field_uid=None):
        self.client = client
        self.global_field_uid = global_field_uid
        super().__init__(self.client)

    def find(self):
        """
        Find the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").global_fields('global_field_uid').find().json()
        -------------------------------
        """
        return self.client.get(_path, headers=self.client.headers, params = self.params)

    def fetch(self):
        """
        Fetches the global fields entry 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').global_fields('global_field_uid').fetch().json()

        -------------------------------
        """
        url = f"{_path}/{self.global_field_uid}"
        return self.client.get(url, headers=self.client.headers, params = self.params)

    def create(self, data):
        """
        Create the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>            "global_field": {
            >>>                "title": "Servlet",
            >>>                "uid": "servlet",
            >>>                "schema": [{
            >>>                    "display_name": "Name",
            >>>                    "uid": "name",
            >>>                    "data_type": "text"
            >>>                }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').global_fields().create(data)
        -------------------------------
        """
        data = json.dumps(data)
        return self.client.post(_path, headers=self.client.headers, data=data, params = self.params)

    def update(self, data):
        """
        Update the global fields entries 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>            "global_field": {
            >>>                "title": "Servlet",
            >>>                "uid": "servlet",
            >>>                "schema": [{
            >>>                    "display_name": "Name",
            >>>                    "uid": "name",
            >>>                    "data_type": "text"
            >>>                }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken="authtoken")
            >>> result = client.stack('api_key').global_fields('global_field_uid').update(data)
        -------------------------------
        """
        url = f"{_path}/{self.global_field_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers=self.client.headers, params=self.params, data=data)

    def delete(self):
        """
        Delete the global fields  
        :return: Json, with status code and message.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken="authtoken")
            >>> result = client.stack('api_key').global_fields('global_field_uid').delete()
        -------------------------------
        """
        url = f"{_path}/{self.global_field_uid}"
        return self.client.delete(url, headers=self.client.headers, params=self.params)

    def imports(self, file_path):
        """
        Import the global fields
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken="authtoken")
            >>> path = "tests/resources/mock_global_fields/import_global_fields.json"
            >>> result = client.stack('api_key').global_fields().imports(path)
        -------------------------------
        """
        self.client.headers['Content-Type'] = "multipart/form-data"
        files = {'global_field': open(f"{file_path}", 'rb')}
        return self.client.post('global_fields/import', headers=self.client.headers, params=self.params, files=files)

    def export(self):
        """
        Export the global fields 
        :return: Json, with global fields details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').global_fields().export().json()
        -------------------------------
        """
        if self.global_field_uid is None or '':
            raise Exception('global_field_uid is required')
        url = f"{_path}/{self.global_field_uid}/export"
        return self.client.get(url, headers=self.client.headers, params=self.params)
