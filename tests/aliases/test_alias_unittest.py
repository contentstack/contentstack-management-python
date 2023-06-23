import unittest
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class AliasesUnitTests(unittest.TestCase):

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
        alias_uid = os.getenv("ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(alias_uid).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{alias_uid}")
        self.assertEqual(response.request.method, "GET")
    
    def test_assign_alias(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
                }
            }
        alias_uid = os.getenv("ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(alias_uid).assign(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{alias_uid}")
        self.assertEqual(response.request.method, "PUT")

    def test_delete_alias(self):
        alias_uid = os.getenv("ALIAS_UID2")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(alias_uid).delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branch_aliases/{alias_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")

if __name__ == '__main__':
    unittest.main()