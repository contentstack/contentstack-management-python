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
environments_name = credentials["environments_name"]

class EnvironmentsApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_environments(self):
        response = self.client.stack(api_key).environments().find()
        self.assertEqual(response.status_code, 200)

    def test_get_a_environments(self):
        response = self.client.stack(api_key).environments(environments_name).fetch()
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 201)

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
        self.assertEqual(response.status_code, 200)


    def test_delete_environments(self):
        response = self.client.stack(api_key).environments(environments_name).delete()
        self.assertEqual(response.status_code, 200)

