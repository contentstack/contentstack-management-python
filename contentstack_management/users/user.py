import json

from contentstack_management.common import Parameter

_path = "user"


class User(Parameter):

    def __init__(self, client):
        self.client = client
        super().__init__(self.client)

    def fetch(self):
        """
        The Get user call returns comprehensive information of an existing user account. 
        The information returned includes details of the stacks owned by and 
        shared with the specified user account
        
        :return: User information

        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.user().fetch()
        -------------------------------
        """
        return self.client.get(_path, params=self.params, headers=self.client.headers)

    def update(self, body):
        """
        The function updates a resource by sending a PUT request with the provided body data.
        
        :param body: The `body` parameter is the data that you want to update. It should be a dictionary
        or JSON object containing the updated values for the resource you are updating
        :return: The code is returning the result of the `put` request made using the `self.client.put`
        method.
        -------------------------------
        [Example:]
            >>> body ={
            >>>    "user": {
            >>>       "company": "company name inc.",
            >>>       "first_name": "Your name"
            >>>      }
            >>>   }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> user = client.user()
            >>> result = user.update(body)
        -------------------------------
        """
        
        data = json.dumps(body)
        return self.client.put(_path, headers=self.client.headers, data=data, params=self.params)

    def activate(self, activation_token, body: dict or None):
        """
        The function activates a user account using an activation token and optional body data.
        
        :param activation_token: The `activation_token` parameter is a token that is used to activate a
        user account. It is typically generated when a user signs up or requests an account activation
        :param body: The `body` parameter is a dictionary or `None`. It is used to pass additional data
        or payload to the `activate` method. If `body` is a dictionary, it will be converted to JSON
        format using the `json.dumps()` function before being sent in the request. If `body
        :type body: dict or None
        :return: the result of the `post` request made to the specified URL `_url`.
        -------------------------------
        [Example:]

            >>> body={
            >>>    "user": {
            >>>       "first_name": "first_name",
            >>>       "last_name": "last_name",
            >>>       "password": "password",
            >>>       "password_confirmation": "confirm_password"
            >>>      }
            >>>   }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = self.client.user().activate('user_activation_token', body)
        -------------------------------
        """
        
        
        _url = f"{_path}/activate/{activation_token}"
        data = json.dumps(body)
        return self.client.post(_url, headers=self.client.headers, params=self.params, data=data)

    def forgot_password(self, body):
        """
        The function sends a POST request to the "forgot_password" endpoint with the provided body data.
        
        :param body: The `body` parameter is a dictionary that contains the necessary information for
        the forgot password request. It typically includes the user's email or username
        :return: the result of a POST request to the specified URL with the provided headers,
        parameters, and data.
        -------------------------------
        [Example:]

            >>> payload={
            >>>      "user": {
            >>>         "email": "john.doe@contentstack.com"
            >>>      }
            >>>   }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.user().request_password(payload).json()
        -------------------------------
        """
        
        url = f"{_path}/forgot_password"
        data = json.dumps(body)
        return self.client.post(url, headers=self.client.headers, params=self.params, data=data)

    def reset_password(self, body):
        """
        The function `reset_password` sends a POST request to a specified URL with a JSON body to reset
        a user's password.
        
        :param body: The `body` parameter is a dictionary that contains the necessary information to
        reset a password. It should include the user's email or username, as well as any additional
        information required for the password reset process
        :return: the result of the `self.client.post()` method call.
        -------------------------------
        [Example:]

        >>> data = {
        >>>     "user": {
        >>>     "reset_password_token": "*******",
        >>>     "password": "******",
        >>>     "password_confirmation": "*****"
        >>>    }
        >>>  }
        >>> import contentstack_management
        >>> client = contentstack_management.Client(authtoken='your_authtoken')
        
        >>> result = client.user().reset_password(body).json()
        -------------------------------
        """
        url = f"{_path}/reset_password"
        body = json.dumps(body)
        return self.client.post(url, headers=self.client.headers, params=self.params, data=body)
