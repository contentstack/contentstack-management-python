import json

_path = "user-session"


def authtoken(response):
    return response['user']['authtoken']


class UserSession:
    """
    User session consists of calls that will help you to sign in 
    and sign out of your Contentstack account.
    """

    def __init__(self, client=None):
        """
        The function initializes an object with a client and retrieves the authtoken from the client's
        headers.
        
        :param client: The `client` parameter is an object that represents a client connection to a
        server. It is typically used to make HTTP requests to the server and handle the responses. In
        this code snippet, the `client` object is expected to have a `headers` attribute, which is
        assumed to be a dictionary
        """
        self.client = client
        if 'authtoken' in self.client.headers:
            self.authtoken = self.client.headers['authtoken']
        else:
            self.authtoken = None


    def login(self, email=None, password=None, tfa_token=None):
        """
        The login function takes in an email, password, and optional two-factor authentication token,
        and sends a POST request to the server to authenticate the user.
        
        The Log in to your account request is used to sign in to your Contentstack account and obtain the authtoken.

        :param email: The email parameter is used to pass the user's email address for authentication
        during the login process
        :param password: The password parameter is used to pass the user's password for authentication
        :param tfa_token: The `tfa_token` parameter is used for two-factor authentication. It is an
        optional parameter that can be provided if the user has enabled two-factor authentication for
        their account. The `tfa_token` is a token generated by the user's authenticator app or received
        via SMS, and it is
        :return: the response object.
        """
        
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
        """
        The above function logs out the user by deleting the authtoken from the client headers.
        :return: the response object.
        """

        self.client.headers.update['authtoken'] = self.authtoken
        response = self.client.delete(_path, headers=self.client.headers, params=None, json_data=None)
        if response.status_code == 200:
            self.client.headers['authtoken'] = None
        return response
