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
label_uid = credentials["label_uid"]

class LabelApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_label(self):
        response = self.client.stack(api_key).label().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}labels")
        self.assertEqual(response.status_code, 200)

    def test_get_a_label(self):
        response = self.client.stack(api_key).label(label_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}labels/{label_uid}")
        self.assertEqual(response.status_code, 200)


    def test_create(self):
        data = {
                "label": {
                    "name": "Test",
                    "parent": [
                    "label_uid"
                    ],
                    "content_types": [
                    "content_type_uid"
                    ]
                }
                }
        response = self.client.stack(api_key).label().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}labels")
        self.assertEqual(response.status_code, 201)

    def test_update_label(self):
        data = {
                "label": {
                    "name": "Test",
                    "parent": [
                    "label_uid"
                    ],
                    "content_types": [
                    "content_type_uid"
                    ]
                }
                }
        response = self.client.stack(api_key).label(label_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}labels/{label_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_label(self):
        response = self.client.stack(api_key).label(label_uid).delete()
        self.assertEqual(response.status_code, 200)

    