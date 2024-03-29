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
metadata_uid = credentials["metadata_uid"]

class MetadataApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_metadata(self):
        response = self.client.stack(api_key).metadata().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}metadata")
        self.assertEqual(response.status_code, 200)

    def test_get_a_metadata(self):
        response = self.client.stack(api_key).metadata(metadata_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}metadata/{metadata_uid}")
        self.assertEqual(response.status_code, 200)


    def test_create(self):
        data = {
                    "metadata": {
                        "entity_uid": "entity_uid",
                        "type": "entry",
                        "_content_type_uid": "_content_type_uid",
                        "extension_uid": "extension_uid",
                        "presets": [{
                            "uid": "presents_uid",
                            "name": "Test1",
                            "options": {

                            }
                        }]
                    }
                }
        response = self.client.stack(api_key).metadata().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}metadata")
        self.assertEqual(response.status_code, 201)

    def test_update_metadata(self):
        data = {
                "metadata": {
                    "entity_uid": "entity_uid",
                    "type": "entry",
                    "_content_type_uid": "_content_type_uid",
                    "extension_uid": "extension_uid",
                    "presets": [{
                        "uid": "presents_uid",
                        "name": "Test1",
                        "options": {

                        }
                    }]
                }
            }
        response = self.client.stack(api_key).metadata(metadata_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}metadata/{metadata_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_metadata(self):
        response = self.client.stack(api_key).metadata(metadata_uid).delete()
        self.assertEqual(response.status_code, 200)

    def test_publish(self):
        data = {
            "metadata": {
                "environments": [
                "environment_name"
                ],
                "locales": [
                "en-us"
                ]
            }
        }
        response = self.client.stack(api_key).metadata(metadata_uid).publish(data)
        self.assertEqual(response.status_code, 200)

    def test_unpublish(self):
        data = {
            "metadata": {
                "environments": [
                "environment_name"
                ],
                "locales": [
                "en-us"
                ]
            }
        }
        response = self.client.stack(api_key).metadata(metadata_uid).unpublish(data)
        self.assertEqual(response.status_code, 200)

    