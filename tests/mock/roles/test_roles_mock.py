import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
role_uid = credentials["role_uid"]


class rolesMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_roles/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_roles(self):
        response = self.client.stack(api_key).roles().find().json()
        read_mock_roles_data  = self.read_file("find.json")
        mock_roles_data = json.loads(read_mock_roles_data)
        self.assertEqual(mock_roles_data.keys(), response.keys())

    def test_get_a_roles(self):
        response = self.client.stack(api_key).roles(role_uid).fetch().json()
        read_mock_roles_data  = self.read_file("fetch.json")
        mock_roles_data = json.loads(read_mock_roles_data)
        self.assertEqual(mock_roles_data.keys(), response.keys())

    def test_create(self):
        data = {
                "role":{
                    "name":"testRole",
                    "description":"This is a test role.",
                    "rules":[
                    {
                        "module":"branch",
                        "branches":[
                        "main"
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
                    },
                    {
                        "module":"content_type",
                        "content_types":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "sub_acl":{
                            "read":True
                        }
                        }
                    },
                    {
                        "module":"asset",
                        "assets":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "update":True,
                        "publish":True,
                        "delete":True
                        }
                    },
                    {
                        "module":"folder",
                        "folders":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "sub_acl":{
                            "read":True
                        }
                        }
                    },
                    {
                        "module":"environment",
                        "environments":[
                        "$all"
                        ],
                        "acl":{
                        "read":True
                        }
                    },
                    {
                        "module":"locale",
                        "locales":[
                        "en-us"
                        ],
                        "acl":{
                        "read":True
                        }
                    },
                    {
                        "module": "taxonomy",
                        "taxonomies": ["taxonomy_testing1"],
                        "terms": ["taxonomy_testing1.term_test1"],
                        "content_types": [
                        {
                            "uid": "$all",
                            "acl": {
                            "read": True,
                            "sub_acl": {
                                "read": True,
                                "create": True,
                                "update": True,
                                "delete": True,
                                "publish": True
                            }
                            }
                        }
                        ],
                        "acl": {
                        "read": True,
                        "sub_acl": {
                            "read": True,
                            "create": True,
                            "update": True,
                            "delete": True,
                            "publish": True
                        }
                        }
                    }
                    ]
                }
                }

        response = self.client.stack(api_key).roles().create(data).json()
        read_mock_roles_data  = self.read_file("create.json")
        mock_roles_data = json.loads(read_mock_roles_data)
        self.assertEqual(mock_roles_data.keys(), response.keys())

    def test_update_roles(self):
        data = {
                "role":{
                    "name":"sampleRole",
                    "description":"This is a test role.",
                    "rules":[
                    {
                        "module":"branch",
                        "branches":[
                        "main"
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
                    },
                    {
                        "module":"content_type",
                        "content_types":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "sub_acl":{
                            "read":True
                        }
                        }
                    },
                    {
                        "module":"asset",
                        "assets":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "update":True,
                        "publish":True,
                        "delete":True
                        }
                    },
                    {
                        "module":"folder",
                        "folders":[
                        "$all"
                        ],
                        "acl":{
                        "read":True,
                        "update":True,
                        "publish":True,
                        "delete":True,
                        "sub_acl":{
                            "read":True,
                            "update":True,
                            "publish":True,
                            "delete":True
                        }
                        }
                    },
                    {
                        "module":"environment",
                        "environments":[
                        "$all"
                        ],
                        "acl":{
                        "read":True
                        }
                    },
                    {
                        "module":"locale",
                        "locales":[
                        "$all"
                        ],
                        "acl":{
                        "read":True
                        }
                    }
                    ],
                    "uid":"blt5a570885da41c710"
                }
                }
        response = self.client.stack(api_key).roles(role_uid).update(data).json()
        read_mock_roles_data  = self.read_file("update.json")
        mock_roles_data = json.loads(read_mock_roles_data)
        self.assertEqual(mock_roles_data.keys(), response.keys())

    def test_delete_roles(self):
        response = self.client.stack(api_key).roles(role_uid).delete().json()
        read_mock_roles_data  = self.read_file("delete.json")
        mock_roles_data = json.loads(read_mock_roles_data)
        self.assertEqual(mock_roles_data['notice'], response['notice'])
        
