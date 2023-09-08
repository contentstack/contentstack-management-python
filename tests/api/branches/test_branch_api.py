import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
branch_uid = credentials["branch_uid"]



class BranchApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    def test_get_all_branches(self):    
        response = self.client.stack(api_key).branch().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_a_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_create_branch(self):
        data = {
        "branch": {
            "uid": "release2",
            "source": "main"
            }
        }
        response = self.client.stack(api_key).branch().create(data)
        if response.status_code == 201:
            result_json = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your request to create branch is in progress. Please check organization bulk task queue for more details.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_delete_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).delete()
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your request to delete branch is in progress. Please check organization bulk task queue for more details.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()