"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json

from ..global_fields.global_fields import Globalfields


class Stack:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, api_key):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.api_key = api_key
        self.headers['authtoken'] = self.authtoken

    def fetch(self):
        """
        Fetches the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').fetch().json()

        -------------------------------
        """
        url = "stacks"
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers=self.headers)

    def find(self):
        """
        Fetches the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack().fetch_all().json()

        -------------------------------
        """

        url = "stacks"
        return self.api_client.get(url, headers=self.headers)

    def create(self, organization_uid, data):
        """
        Create the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]
            >>> data = {
                            "stack": {
                                "name": "My New Stack",
                                "description": "My new test stack",
                                "master_locale": "en-us"
                            }
                        }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack().create('ORG_UID', data).json()

        -------------------------------
        """
        url = "stacks"

        self.headers['organization_uid'] = organization_uid
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def update(self, data):
        """
        Update the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]
            >>> data = {
                            "stack": {
                                "name": "My New Stack",
                                "description": "My new test stack",
                                "master_locale": "en-us"
                            }
                        }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').update(data).json()

        -------------------------------
        """
        url = "stacks"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.put(url, headers=self.headers, data=data)

    def delete(self):
        """
        Delete the stacks  
        :return: Json, with status code and message.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').delete().json()

        -------------------------------
        """

        url = "stacks"
        self.headers['api_key'] = self.api_key
        return self.api_client.delete(url, headers=self.headers)

    def users(self):
        """
        Fetches the all users of a stack 
        :return: Json, with users of a stack details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack().fetch_all_user().json()

        -------------------------------
        """

        url = "stacks/users"
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers=self.headers)

    def update_user_role(self, data):
        """
        Update the user roles of the stacks 
        :return: Json, with user roles of stacks details.
        -------------------------------
        [Example:]
            >>> data = {
                        "users": {
                            "user_uid": ["role_uid1", "role_uid2"]
                        }
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').update_user_role(data).json()

        -------------------------------
        """
        url = "stacks/users/roles"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.put(url, headers=self.headers, data=data)

    def transfer_ownership(self, data):
        """
        Transfer owership of the stacks 
        :return: Json, with status code and message.
        -------------------------------
        [Example:]
            >>> data = {
                        "transfer_to": "manager@example.com"
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').stack_transfer_ownership(data).json()

        -------------------------------
        """
        url = "stacks/transfer_ownership"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def accept_ownership(self, user_id, ownership_token):
        """
        Accept ownership of the stack 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').accept_ownership(user_id, ownership_token).json()

        -------------------------------
        """
        url = f"stacks/accept_ownership/{ownership_token}"
        params = {'api_key': self.api_key, 'uid': user_id}
        return self.api_client.get(url, headers=self.headers, params=params)

    def settings(self):
        """
        Fetches the stack settings 
        :return: Json, with stack settings details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').get_stack_settings().json()

        -------------------------------
        """
        url = "stacks/settings"
        self.headers['api_key'] = self.api_key
        return self.api_client.get(url, headers=self.headers)

    def create_settings(self, data):
        """
        Create the stack settings 
        :return: Json, with stack setting details.
        -------------------------------
        [Example:]
            >>> data = {
                        "stack_settings": {
                            "stack_variables": {
                                "enforce_unique_urls": true,
                                "sys_rte_allowed_tags": "style,figure,script",
                                "sys_rte_skip_format_on_paste": "GD:font-size"
                                },
                            "rte": {
                                "cs_only_breakline": true
                            }
                        }
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').create_stack_settings(data).json()

        -------------------------------
        """
        url = "stacks/settings"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def reset_settings(self, data):
        """
        Reset the stack settings
        :return: Json, with stack setting details.
        -------------------------------
        [Example:]
            >>> data = {
                        "stack_settings":{}
                    }               
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').reset_stack_settings(data).json()

        -------------------------------
        """
        url = "stacks/settings/reset"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def share(self, data):
        """
        Share a stack to the users with user roles 
        :return: Json, with status code and message
        -------------------------------
        [Example:]
            >>> data = {
                        "emails": [
                            "manager@example.com"
                        ],
                        "roles": {
                            "manager@example.com": [
                                "abcdefhgi1234567890"
                            ]
                        }
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').share_stack(data).json()

        -------------------------------
        """
        url = "stacks/share"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def unshare(self, data):
        """
        Unshare a stack to the users with user roles 
        :return: Json, with status code and message
        -------------------------------
        [Example:]
            >>> data = {
                        "email": "manager@example.com"
                    }
            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.stack('API_KEY').unshare_stack(data).json()

        -------------------------------
        """
        url = "stacks/unshare"
        self.headers['api_key'] = self.api_key
        data = json.dumps(data)
        return self.api_client.post(url, headers=self.headers, data=data)

    def global_fields(self, global_field_uid=None):
        return Globalfields(self.endpoint, self.authtoken, self.headers, self.api_client, self.api_key,
                            global_field_uid)
