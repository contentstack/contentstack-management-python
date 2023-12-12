import json
import os
import unittest

from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
delivery_token_uid = credentials["delivery_token_uid"]


class delivery_tokenMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_delivery_token/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_delivery_token(self):
        response = self.client.stack(api_key).delivery_token().find().json()
        read_mock_delivery_token_data  = self.read_file("find.json")
        mock_delivery_token_data = json.loads(read_mock_delivery_token_data)
        self.assertEqual(mock_delivery_token_data.keys(), response.keys())

    def test_get_a_delivery_token(self):
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).fetch().json()
        read_mock_delivery_token_data  = self.read_file("fetch.json")
        mock_delivery_token_data = json.loads(read_mock_delivery_token_data)
        self.assertEqual(mock_delivery_token_data.keys(), response.keys())

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
        response = self.client.stack(api_key).delivery_token().create(data).json()
        read_mock_delivery_token_data  = self.read_file("create.json")
        mock_delivery_token_data = json.loads(read_mock_delivery_token_data)
        self.assertEqual(mock_delivery_token_data.keys(), response.keys())

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
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).update(data).json()
        read_mock_delivery_token_data  = self.read_file("update.json")
        mock_delivery_token_data = json.loads(read_mock_delivery_token_data)
        self.assertEqual(mock_delivery_token_data.keys(), response.keys())

    def test_delete_delivery_token(self):
        response = self.client.stack(api_key).delivery_token(delivery_token_uid).delete().json()
        read_mock_delivery_token_data  = self.read_file("delete.json")
        mock_delivery_token_data = json.loads(read_mock_delivery_token_data)
        self.assertEqual(mock_delivery_token_data['notice'], response['notice'])
        

   