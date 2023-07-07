import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack


def load_api_keys():
    load_dotenv()


class AliaseApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)

    def test_get_all_aliases(self):    
        response = self.client.stack(os.getenv("API_KEY")).branch_alias().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_an_alias(self):
        alias_uid_get = os.getenv("ALIAS_UID_GET")
        response = self.client.stack(os.getenv("API_KEY")).branch_alias(alias_uid_get).fetch()
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
        alias_uid = os.getenv("ALIAS_UID2")
        response = self.client.stack(os.getenv("API_KEY")).branch_alias(alias_uid).assign(data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Branch alias assigned successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_delete_alias(self):
        alias_uid = os.getenv("ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branch_alias(alias_uid).delete()
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Branch alias deleted successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()