
class User:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers

    
    def get(self):
        url = "user"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)


    def update_user(self, user_data):
        url = "user"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.put(url, headers = self.headers, data = user_data, params = None)
    
    def active_user(self, user_activation_token, user_data):
        url = f"user/activate/{user_activation_token}"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.post(url, headers = self.headers, data = user_data)
    
    def request_password(self, user_data):
        url = "user/forgot_password"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.post(url, headers = self.headers, data = user_data)
    
    def reset_password(self, user_data):
        url = "user/reset_password"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.post(url, headers = self.headers, data = user_data)