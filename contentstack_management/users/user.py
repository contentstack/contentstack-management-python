import json

from contentstack_management.common import Parameter

_path = "user"


class User(Parameter):

    def __init__(self, client):
        self.client = client
        super().__init__(self.client)

    def find(self):
        """
        Fetches the user entries 
        :return: Json, with user details.
        -------------------------------
        [Example:]
            >>> from contentstack_management import contentstack
            >>> client = contentstack.ContentstackClient(host='host')
            >>> client.login(email="email", password="password")
            >>> result = client.user().find()
        -------------------------------
        """
        return self.client.get(_path, params=self.params, headers=self.client.headers)

    def update(self, body):
        """
        Updated user details.
        :return: Json, with response message.
        -------------------------------
        [Example:]
            >>> update_entry ={
                                    "user": {
                                        "company": "company name inc.",
                                        "first_name": "sunil B Lakshman"
                                    }
                                }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.ContentstackClient(host='host')
            >>> user = client.user()
            >>> result = user.update(update_entry)
        -------------------------------
        """
        data = json.dumps(body)
        return self.client.put(_path, headers=self.client.headers, data=data, params=self.params)

    def activate(self, activation_token, body):
        """
        Activate user
        :return: Json, with response message.
        -------------------------------
        [Example:]

            >>> act_data={
            >>>      "user": {
            >>>           "first_name": "first_name",
            >>>            "last_name": "last_name",
            >>>             "password": "password",
            >>>             "password_confirmation": "confirm_password"
            >>>           }
            >>>        }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.ContentstackClient(host='host')
            >>> client.login(email="email", password="password")
            >>> result = self.client.user().active_user('user_activation_token', act_data).json()
        -------------------------------
        """
        activate_url = f"{_path}/activate/{activation_token}"
        data = json.dumps(body)
        return self.client.post(activate_url, headers=self.client.headers, params=self.params, data=data)

    def forgot_password(self, body):
        """
        Requested password
        :return: Json, with response message.
        -------------------------------
        [Example:]

            >>> payload={
            >>>      "user": {
            >>>             "email": "john.doe@contentstack.com"
            >>>       }
            >>>   }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.ContentstackClient(host='host')
            >>> client.login(email="email", password="password")
            >>> result = client.user().request_password(payload).json()
        -------------------------------
        """
        url = f"{_path}/forgot_password"
        data = json.dumps(body)
        return self.client.post(url, headers=self.client.headers, params=self.params, data=data)

    def reset_password(self, body):
        """
        Reset user password 
        :return: Json, with response message.
        -------------------------------
        [Example:]
       >>>
        >>> data = {
        >>>     "user": {
        >>>     "reset_password_token": "*******",
        >>>     "password": "******",
        >>>     "password_confirmation": "*****"
        >>>    }
        >>>  }
        >>> from contentstack_management import contentstack
        >>> client = contentstack.ContentstackClient(host='host')
        >>> client.login(email="email", password="password")
        >>> result = client.user().reset_password(body).json()
        -------------------------------
        """
        url = f"{_path}/reset_password"
        body = json.dumps(body)
        return self.client.post(url, headers=self.client.headers, params=self.params, data=body)
