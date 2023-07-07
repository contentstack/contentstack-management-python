import json


class UserSession:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, username=None, password=None, api_client=None):
        self.headers = api_client.headers
        self.api_client = api_client
        self.endpoint = api_client.endpoint
        self.email = username
        self.password = password
        self.authtoken = api_client.authtoken

    def login(self):
        if self.email is None or self.email == '':
            raise PermissionError(
                'You are not permitted to the stack without valid email id')

        if self.password is None or self.password == '':
            raise PermissionError(
                'You are not permitted to the stack without valid password')

        url = "user-session"
        data = {
            "user": {
                "email": self.email,
                "password": self.password

            }
        }
        data = json.dumps(data)
        response = self.api_client.post(url, headers=self.headers, data=data, json_data=None)
        self.auth_token = self.get_authtoken(response.json()) if response.status_code == 200 else self.authtoken
        return response

    def logout(self):
        url = "user-session"
        self.headers['authtoken'] = self.auth_token
        response = self.api_client.delete(url, headers=self.headers, params=None, json_data=None)
        return response

    def get_authtoken(self, response):
        return response['user']['authtoken']
