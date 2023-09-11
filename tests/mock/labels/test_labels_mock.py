import json
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
label_uid = credentials["label_uid"]


class LabelMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_labels/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_label(self):
        response = self.client.stack(api_key).label().find().json()
        read_mock_label_data  = self.read_file("find.json")
        mock_label_data = json.loads(read_mock_label_data)
        self.assertEqual(mock_label_data.keys(), response.keys())

    def test_get_a_label(self):
        response = self.client.stack(api_key).label(label_uid).fetch().json()
        read_mock_label_data  = self.read_file("fetch.json")
        mock_label_data = json.loads(read_mock_label_data)
        self.assertEqual(mock_label_data.keys(), response.keys())

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
        response = self.client.stack(api_key).label().create(data).json()
        read_mock_label_data  = self.read_file("create.json")
        mock_label_data = json.loads(read_mock_label_data)
        self.assertEqual(mock_label_data.keys(), response.keys())

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
        response = self.client.stack(api_key).label(label_uid).update(data).json()
        read_mock_label_data  = self.read_file("update.json")
        mock_label_data = json.loads(read_mock_label_data)
        self.assertEqual(mock_label_data.keys(), response.keys())

    def test_delete_label(self):
        response = self.client.stack(api_key).label(label_uid).delete().json()
        read_mock_label_data  = self.read_file("delete.json")
        mock_label_data = json.loads(read_mock_label_data)
        self.assertEqual(mock_label_data['notice'], response['notice'])
        