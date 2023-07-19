import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
branch_uid = credentials["branch_uid"]


class BranchesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_branches(self):
        response = self.client.stack(api_key).branch().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches?limit=2&skip=2&include_count"
                                               f"=false")
        self.assertEqual(response.request.method, "GET")

    def test_get_a_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "GET")

    def test_create_branch(self):
        data = {
            "branch": {
                "uid": "release",
                "source": "main"
            }
        }
        response = self.client.stack(api_key).branch().create(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches")
        self.assertEqual(response.request.method, "POST")

    def test_delete_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")
