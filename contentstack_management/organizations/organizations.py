
import json

class Organization:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, authtoken, headers, api_client, organization_uid):
        self.api_client = api_client
        self.endpoint = endpoint
        self.authtoken = authtoken
        self.headers = headers
        self.organization_uid = organization_uid

    
    def get(self):
        """
        Fetches the organizations entries 
        :return: Json, with organizations details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations().get().json()

            >>> result = client.organizations('ORG_UID').get().json()

        -------------------------------
        """
        url = "organizations"
        if self.organization_uid is None:
            url = "organizations"
        else:
            url = f"organizations/{self.organization_uid}"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def get_organization_roles(self):
        """
        Fetches the organization roles entries 
        :return: Json, with organization role details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations('ORG_UID').get_organization_roles().json()

        -------------------------------
        """
        url = f"organizations/{self.organization_uid}/roles"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def organization_add_users(self, user_data):
        """
        Add user to the organization 
        :return: Json, with user details.
        -------------------------------
        [Example:]
            >>> data = {
                        "share": {
                            "users": {
                                "abc@sample.com": ["{{orgAdminRoleUid}}"],
                                "xyz@sample.com": ["{{orgMemberRoleUid}}"]
                            },
                            "stacks": {
                                "abc@sample.com": {
                                    "{{apiKey}}": ["{{stackRoleUid1}}"]
                                },
                                "xyz@sample.com": {
                                    "blta1ed1f11111c1eb1": ["blt111d1b110111e1f1"],
                                    "bltf0c00caa0f0000f0": ["bltcea22222d2222222", "blt333f33cb3e33ffde"]
                                }
                            },
                            "message": "Invitation message"
                        }
                    }

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations('ORG_UID').organization_add_users(data).json()

        -------------------------------
        """
        url = f"organizations/{self.organization_uid}/share"
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(user_data)
        return self.api_client.post(url, headers = self.headers, data = data)
    
    def transfer_organizations_ownership(self, data):
        """
        Add user to the organization 
        :return: Json, with user details.
        -------------------------------
        [Example:]
            >>> data ={
                        "transfer_to": "abc@sample.com"
                    }

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations('ORG_UID').transfer_organizations_ownership(data).json()

        -------------------------------
        """

        url = f"organizations/{self.organization_uid}/transfer-ownership"
        self.headers['authtoken'] = self.authtoken
        data = json.dumps(data)
        return self.api_client.post(url, headers = self.headers, data = data)

    
    def organization_stacks(self):
        """
        Fetches the organization stacks 
        :return: Json, with organization stack details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations('ORG_UID').organization_stacks().json()

        -------------------------------
        """
        url = f"organizations/{self.organization_uid}/stacks"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

    
    def organization_logs(self):
        """
        Fetches the organization log entries 
        :return: Json, with organization log details.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> client.login(email="email_id", password="password")
            >>> result = client.organizations('ORG_UID').organization_logs().json()

        -------------------------------
        """
        url = f"organizations/{self.organization_uid}/logs"
        self.headers['authtoken'] = self.authtoken
        return self.api_client.get(url, headers = self.headers)

