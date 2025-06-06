import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
taxonomy_uid = credentials["taxonomy_uid"]

class taxonomyUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_taxonomy(self):
        response = self.client.stack(api_key).taxonomy().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_all_taxonomy_with_add_param(self):
        query = self.client.stack(api_key).taxonomy()
        query.add_param("include_branch", True)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies?include_branch=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)


    def test_get_a_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}taxonomies/{taxonomy_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create(self):
        data = {
            "taxonomy": {
                "uid": "taxonomy_1",
                "name": "Taxonomy 1",
                "description": "Description for Taxonomy 1"
            }
            }
        response = self.client.stack(api_key).taxonomy().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_taxonomy(self):
        data = {
                "taxonomy": {
                    "name": "Taxonomy 1",
                    "description": "Description updated for Taxonomy 1"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}taxonomies/{taxonomy_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_delete_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}")
        self.assertEqual(response.request.method, "DELETE")
