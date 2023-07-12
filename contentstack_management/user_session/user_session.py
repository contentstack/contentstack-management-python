import json

_path = "user-session"


def authtoken(response):
    return response['user']['authtoken']


class UserSession:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API
    """

    def __init__(self, client=None):
        self.client = client
        self.authtoken = self.client.headers['authtoken']

    def login(self, email=None, password=None, tfa_token=None):
        if email is None or email == '':
            raise PermissionError(
                'Email Id is required')

        if password is None or password == '':
            raise PermissionError(
                'Password is required')

        data = {
            "user": {
                "email": email,
                "password": password,
            }
        }

        if tfa_token is not None:
            data["user"]["tf_token"] = tfa_token

        data = json.dumps(data)
        response = self.client.post(_path, headers=self.client.headers, data=data, json_data=None)
        if response.status_code == 200:
            res = response.json()
            self.client.headers['authtoken'] = res['user']['authtoken']
        return response

    def logout(self):
        self.client.headers.update['authtoken'] = self.authtoken
        response = self.client.delete(_path, headers=self.client.headers, params=None, json_data=None)
        if response.status_code == 200:
            self.client.headers['authtoken'] = None
        return response
