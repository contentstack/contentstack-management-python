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
management_token_uid = credentials["management_token_uid"]


class management_tokenMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_management_token/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_management_token(self):
        response = self.client.stack(api_key).management_token().find().json()
        read_mock_management_token_data  = self.read_file("find.json")
        mock_management_token_data = json.loads(read_mock_management_token_data)
        self.assertEqual(mock_management_token_data.keys(), response.keys())

    def test_get_a_management_token(self):
        response = self.client.stack(api_key).management_token(management_token_uid).fetch().json()
        read_mock_management_token_data  = self.read_file("fetch.json")
        mock_management_token_data = json.loads(read_mock_management_token_data)
        self.assertEqual(mock_management_token_data.keys(), response.keys())

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
        response = self.client.stack(api_key).management_token().create(data).json()
        read_mock_management_token_data  = self.read_file("create.json")
        mock_management_token_data = json.loads(read_mock_management_token_data)
        self.assertEqual(mock_management_token_data.keys(), response.keys())

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
        response = self.client.stack(api_key).management_token(management_token_uid).update(data).json()
        read_mock_management_token_data  = self.read_file("update.json")
        mock_management_token_data = json.loads(read_mock_management_token_data)
        self.assertEqual(mock_management_token_data.keys(), response.keys())

    def test_delete_management_token(self):
        response = self.client.stack(api_key).management_token(management_token_uid).delete().json()
        read_mock_management_token_data  = self.read_file("delete.json")
        mock_management_token_data = json.loads(read_mock_management_token_data)
        self.assertEqual(mock_management_token_data['notice'], response['notice'])
        