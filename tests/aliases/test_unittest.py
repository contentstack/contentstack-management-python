import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class AliasesTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)

    def test_get_all_aliases(self):
        response = self.client.stack(os.getenv("API_KEY")).branchAlias().fetchAll()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases?limit=2&skip=2&include_count=false")
        self.assertEqual(response.request.method, "GET")
    
    def test_get_an_alias(self):
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{branch_alias_uid}")
        self.assertEqual(response.request.method, "GET")
    
    def test_create_or_update(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
                }
            }
        branch_test_uid = os.getenv("BRANCH_TEST_UID")
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).createOrUpdate(branch_test_uid, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{branch_alias_uid}")
        self.assertEqual(response.request.method, "PUT")

    def test_delete_alias(self):
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{branch_alias_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")