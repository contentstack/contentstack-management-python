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

class rolesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_roles(self):
        response = self.client.stack(api_key).roles().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}roles")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_roles(self):
        response = self.client.stack(api_key).roles(role_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}roles/{role_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

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

        response = self.client.stack(api_key).roles().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}roles")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

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
                    "uid":"role_uid"
                }
                }
        response = self.client.stack(api_key).roles(role_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}roles/{role_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_delete_roles(self):
        response = self.client.stack(api_key).roles(role_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}roles/{role_uid}")
        self.assertEqual(response.request.method, "DELETE")
