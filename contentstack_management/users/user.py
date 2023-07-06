
import json

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
        self.headers['authtoken'] = authtoken

    
    def find(self):
        """
        Fetches the user entries 
        :return: Json, with user details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.user().get().json()

        -------------------------------
        """
        url = "user"
       
        return self.api_client.get(url, headers = self.headers)


    def update(self, user_data):
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
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.update_user(update_entry)
        -------------------------------
        """
        url = "user"
        data = json.dumps(user_data)
        return self.api_client.put(url, headers = self.headers, data = data, params = None)
    
    def activate(self, user_activation_token, user_data):
        """
        Activate user
        :return: Json, with response message.
        -------------------------------
        [Example:]

            >>> act_data={
                            "user": {
                                "first_name": "your_first_name",
                                "last_name": "your_last_name",
                                "password": "your_password",
                                "password_confirmation": "confirm_your_password"
                                }
                            }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.user().active_user('user_activation_token',act_data).json()
        -------------------------------
        """
        url = f"user/activate/{user_activation_token}"
        data = json.dumps(user_data)
        return self.api_client.post(url, headers = self.headers, data = data)
    
    def forgot_password(self, user_data):
        """
        Requested password
        :return: Json, with response message.
        -------------------------------
        [Example:]

            >>> user_data={
                            "user": {
                                "email": "john.doe@contentstack.com"
                            }
                        }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.user().request_password(user_data).json()
        -------------------------------
        """
        url = "user/forgot_password"
        data = json.dumps(user_data)
        return self.api_client.post(url, headers = self.headers, data = data)
    
    def reset_password(self, user_data):
        """
        Reset user password 
        :return: Json, with response message.
        -------------------------------
        [Example:]

           >>> user_data={
                            "user": {
                                "reset_password_token": "abcdefghijklmnop1234567890",
                                "password": "Simple@123",
                                "password_confirmation": "Simple@123"
                            }
                        }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.user().reset_password(user_data).json()
        -------------------------------
        """
        url = "user/reset_password"
        data = json.dumps(user_data)
        return self.api_client.post(url, headers = self.headers, data = data)