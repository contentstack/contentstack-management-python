import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
extension_uid = credentials["extension_uid"]


class ExtensionMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_extension/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_extension(self):
        response = self.client.stack(api_key).extension().find().json()
        read_mock_extension_data  = self.read_file("find.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data.keys(), response.keys())

    def test_get_a_extension(self):
        response = self.client.stack(api_key).extension(extension_uid).fetch().json()
        read_mock_extension_data  = self.read_file("fetch.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data.keys(), response.keys())

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
        response = self.client.stack(api_key).extension().create(extension).json()
        read_mock_extension_data  = self.read_file("create.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data.keys(), response.keys())

    def test_upload(self):
        extension = {
                    "file_name": "demo.html",
                    "file_path": "/Users/sunil.lakshman/Downloads/demo.html",
                    "data_type": 'text',
                    "title": 'Old Extension',
                    "multiple": False,
                    "tags": {},
                    "type": 'dashboard'
                    }
        response = self.client.stack(api_key).extension().update(extension).json()
        read_mock_extension_data  = self.read_file("create.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data.keys(), response.keys())

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
        response = self.client.stack(api_key).extension(extension_uid).update(extension).json()
        read_mock_extension_data  = self.read_file("update.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data.keys(), response.keys())

    def test_delete_extension(self):
        response = self.client.stack(api_key).extension(extension_uid).delete().json()
        read_mock_extension_data  = self.read_file("delete.json")
        mock_extension_data = json.loads(read_mock_extension_data)
        self.assertEqual(mock_extension_data['notice'], response['notice'])
        