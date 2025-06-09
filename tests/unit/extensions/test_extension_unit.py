import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
extension_uid = credentials["extension_uid"]

class extensionUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_extension(self):
        response = self.client.stack(api_key).extension().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}extensions")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_extension(self):
        response = self.client.stack(api_key).extension(extension_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}extensions/{extension_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create(self):
        extension = {
            "extension": {
                "tags": [
                    "tag1",
                    "tag2"
                ],
                "data_type": "text",
                "title": "New Custom Field",
                "src": "https://www.sample.com",
                "multiple": False,
                "config": "{}",
                "type": "field"
            }
        }
        response = self.client.stack(api_key).extension().create(extension)
        self.assertEqual(response.request.url, f"{self.client.endpoint}extensions")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_extension(self):
        extension = {
            "extension": {
                "tags": [
                    "tag1",
                    "tag2"
                ],
                "data_type": "text",
                "title": "New Custom Field",
                "src": "https://www.sample.com",
                "multiple": False,
                "config": "{}",
                "type": "field"
            }
        }
        response = self.client.stack(api_key).extension(extension_uid).update(extension)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}extensions/{extension_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_delete_extension(self):
        response = self.client.stack(api_key).extension(extension_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}extensions/{extension_uid}")
        self.assertEqual(response.request.method, "DELETE")


    