import os
import unittest
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
taxonomy_uid = credentials["taxonomy_uid"]



class TaxonomyApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_taxonomy(self):
        response = self.client.stack(api_key).taxonomy().find()
        self.assertEqual(response.status_code, 200)

    def test_get_a_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).fetch()
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
                "taxonomy": {
                    "uid": "taxonomy_1",
                    "name": "Taxonomy 1",
                    "description": "Description for Taxonomy 1"
                }
                }
        response = self.client.stack(api_key).taxonomy().create(data)
        self.assertEqual(response.status_code, 201)

    def test_update_taxonomy(self):
        data = {
                "taxonomy": {
                    "name": "Taxonomy 1",
                    "description": "Description updated for Taxonomy 1"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).update(data)
        self.assertEqual(response.status_code, 200)


    def test_delete_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).delete()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
