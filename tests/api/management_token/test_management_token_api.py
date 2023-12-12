import os
import unittest
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
management_token_uid = credentials["management_token_uid"]

class ManagementTokenUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_management_token(self):
        response = self.client.stack(api_key).management_token().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/management_tokens")
        self.assertEqual(response.status_code, 200)

    def test_get_a_management_token(self):
        response = self.client.stack(api_key).management_token(management_token_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/management_tokens/{management_token_uid}")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
                "token":{
                    "name":"Test Token",
                    "description":"This is a sample management token.",
                    "scope":[
                        {
                            "module":"content_type",
                            "acl":{
                                "read":True,
                                "write":True
                            }
                        },
                        {
                            "module":"branch",
                            "branches":[
                                "main",
                                "development"
                            ],
                            "acl":{
                                "read":True
                            }
                        },
                        {
                            "module":"branch_alias",
                            "branch_aliases":[
                                "deploy",
                                "release"
                            ],
                            "acl":{
                                "read":True
                            }
                        }
                    ],
                    "expires_on":"2020-12-10",
                    "is_email_notification_enabled":True
                }
            }
        response = self.client.stack(api_key).management_token().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/management_tokens")
        self.assertEqual(response.status_code, 201)

    def test_update_management_token(self):
        data = {
                "token":{
                    "name":"Updated Test Token",
                    "description":"This is an updated management token.",
                    "scope":[
                        {
                            "module":"content_type",
                            "acl":{
                                "read":True,
                                "write":True
                            }
                        },
                        {
                            "module":"entry",
                            "acl":{
                                "read":True,
                                "write":True
                            }
                        },
                        {
                            "module":"branch",
                            "branches":[
                                "main",
                                "development"
                            ],
                            "acl":{
                                "read":True
                            }
                        },
                        {
                            "module":"branch_alias",
                            "branch_aliases":[
                                "deploy"
                            ],
                            "acl":{
                                "read":True
                            }
                        }
                    ],
                    "expires_on":"2020-12-31",
                    "is_email_notification_enabled":True
                }
            }
        response = self.client.stack(api_key).management_token(management_token_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/management_tokens/{management_token_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_management_token(self):
        response = self.client.stack(api_key).management_token(management_token_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/management_tokens/{management_token_uid}")
        self.assertEqual(response.status_code, 200)