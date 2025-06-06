import unittest


import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
branch_uid = credentials["branch_uid"]


class BranchesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_branches(self):
        response = self.client.stack(api_key).branch().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_branch(self):
        data = {
            "branch": {
                "uid": "release",
                "source": "main"
            }
        }
        response = self.client.stack(api_key).branch().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
