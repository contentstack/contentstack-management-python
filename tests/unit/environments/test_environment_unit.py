import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
environments_name = credentials["environments_name"]

class EnvironmentsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_environments(self):
        response = self.client.stack(api_key).environments().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}environments")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_environments(self):
        response = self.client.stack(api_key).environments(environments_name).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}environments/{environments_name}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create(self):
        data = {
                    "environment": {
                        "name": "test",
                        "urls": [{
                            "locale": "en-us",
                            "url": "http://example.com/"
                        }]
                    }
                }
        response = self.client.stack(api_key).environments().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}environments")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_environments(self):
        data = {
                    "environment": {
                        "name": "test",
                        "urls": [{
                            "locale": "en-us",
                            "url": "http://example.com/"
                        }]
                    }
                }
        response = self.client.stack(api_key).environments(environments_name).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}environments/{environments_name}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_delete_environments(self):
        response = self.client.stack(api_key).environments(environments_name).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}environments/{environments_name}")
        self.assertEqual(response.request.method, "DELETE")

