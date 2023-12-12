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
role_uid = credentials["role_uid"]

class rolesApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_roles(self):
        response = self.client.stack(api_key).roles().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}roles")
        self.assertEqual(response.status_code, 200)

    def test_get_a_roles(self):
        response = self.client.stack(api_key).roles(role_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}roles/{role_uid}")
        self.assertEqual(response.status_code, 200)


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
                    }
                    ]
                }
                }

        response = self.client.stack(api_key).roles().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}roles")
        self.assertEqual(response.status_code, 201)

    def test_update_roles(self):
        data = data = {
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
        response = self.client.stack(api_key).roles(role_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}roles/{role_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_roles(self):
        response = self.client.stack(api_key).roles(role_uid).delete()
        self.assertEqual(response.status_code, 200)

    