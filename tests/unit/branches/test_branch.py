import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack


def load_api_keys():
    load_dotenv()


class BranchesUnitTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(email, password)

    def test_get_all_branches(self):
        response = self.client.stack(os.getenv("API_KEY")).branch().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branches?limit=2&skip=2&include_count"
                                               f"=false")
        self.assertEqual(response.request.method, "GET")

    def test_get_a_branch(self):
        branch_uid = os.getenv("BRANCH_UID_GET")
        response = self.client.stack(os.getenv("API_KEY")).branch(branch_uid).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "GET")

    def test_create_branch(self):
        data = {
            "branch": {
                "uid": "release",
                "source": "main"
            }
        }
        response = self.client.stack(os.getenv("API_KEY")).branch().create(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branches")
        self.assertEqual(response.request.method, "POST")

    def test_delete_branch(self):
        branch_uid = os.getenv("BRANCH_UID_DEL")
        response = self.client.stack(os.getenv("API_KEY")).branch(branch_uid).delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/branches/{branch_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")
