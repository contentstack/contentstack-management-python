import unittest
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class BranchApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)

    def test_get_all_branches(self):    
        response = self.client.stack(os.getenv("API_KEY")).branch().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_a_branch(self):
        branch_uid = os.getenv("BRANCH_UID")
        response = self.client.stack(os.getenv("API_KEY")).branch(branch_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_create_branch(self):
        data = {
        "branch": {
            "uid": "release",
            "source": "main"
            }
        }
        response = self.client.stack(os.getenv("API_KEY")).branch().create(data)
        if response.status_code == 201:
            result_json = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your request to create branch is in progress. Please check organization bulk task queue for more details.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_delete_branch(self):
        branch_uid = os.getenv("BRANCH_UID")
        response = self.client.stack(os.getenv("API_KEY")).branch(branch_uid).delete()
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your request to delete branch is in progress. Please check organization bulk task queue for more details.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()