import os
import unittest
from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
alias_uid = credentials["alias_uid"]


class AliasesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_aliases(self):
        response = self.client.stack(api_key).branch_alias().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/branch_aliases?limit=2&skip=2")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_an_alias(self):
        response = self.client.stack(api_key).branch_alias(alias_uid).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branch_aliases/{alias_uid}")
        self.assertEqual(response.request.method, "GET")

    def test_assign_alias(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
            }
        }
        response = self.client.stack(api_key).branch_alias(alias_uid).assign(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branch_aliases/{alias_uid}")
        self.assertEqual(response.request.method, "PUT")

    def test_delete_alias(self):
        response = self.client.stack(api_key).branch_alias(alias_uid).delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branch_aliases/{alias_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")


if __name__ == '__main__':
    unittest.main()
