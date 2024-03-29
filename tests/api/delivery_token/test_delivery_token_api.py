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
delivery_token_uid = credentials["delivery_token_uid"]

class DeliveryTokenUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_delivery_token(self):
        response = self.client.stack(api_key).delivery_token().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/delivery_tokens")
        self.assertEqual(response.status_code, 200)
        

    def test_get_a_delivery_token(self):
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/delivery_tokens/{delivery_token_uid}")
        self.assertEqual(response.status_code, 200)
        

    def test_create(self):
        data = {
                "token":{
                    "name":"Test",
                    "description":"This is a demo token.",
                    "scope":[
                        {
                            "module":"environment",
                            "environments":[
                                "production"
                            ],
                            "acl":{
                                "read":True
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
                    ]
                }
            }
        response = self.client.stack(api_key).delivery_token().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/delivery_tokens")
        self.assertEqual(response.status_code, 201)

    def test_update_delivery_token(self):
        data = {
                "token":{
                    "name":"Test",
                    "description":"This is a updated token.",
                    "scope":[
                        {
                            "module":"environment",
                            "environments":[
                                "production"
                            ],
                            "acl":{
                                "read":True
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
                    ]
                }
            }
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/delivery_tokens/{delivery_token_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_delivery_token(self):
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/delivery_tokens/{delivery_token_uid}")
        self.assertEqual(response.status_code, 200)

    