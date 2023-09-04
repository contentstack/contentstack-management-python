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
alias_uid = credentials["alias_uid"]


class AliaseApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    def test_get_all_aliases(self):    
        response = self.client.stack(api_key).alias().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_an_alias(self):
        response = self.client.stack(api_key).alias(alias_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_assign_alias(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
                }
            }
        response = self.client.stack(api_key).alias(alias_uid).assign(data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Branch alias assigned successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_delete_alias(self):
        response = self.client.stack(api_key).alias(alias_uid).delete()
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Branch alias deleted successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()