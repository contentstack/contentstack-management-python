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
metadata_uid = credentials["metadata_uid"]


class metadataMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_metadata/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_metadata(self):
        response = self.client.stack(api_key).metadata().find().json()
        read_mock_metadata_data  = self.read_file("find.json")
        mock_metadata_data = json.loads(read_mock_metadata_data)
        self.assertEqual(mock_metadata_data.keys(), response.keys())

    def test_get_a_metadata(self):
        response = self.client.stack(api_key).metadata(metadata_uid).fetch().json()
        read_mock_metadata_data  = self.read_file("fetch.json")
        mock_metadata_data = json.loads(read_mock_metadata_data)
        self.assertEqual(mock_metadata_data.keys(), response.keys())

    def test_create(self):
        data = {
                    "metadata": {
                        "entity_uid": "entry_uid",
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
        response = self.client.stack(api_key).metadata().create(data).json()
        read_mock_metadata_data  = self.read_file("create.json")
        mock_metadata_data = json.loads(read_mock_metadata_data)
        self.assertEqual(mock_metadata_data.keys(), response.keys())

    def test_update_metadata(self):
        data = {
                    "metadata": {
                        "entity_uid": "entry_uid",
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
        response = self.client.stack(api_key).metadata(metadata_uid).update(data).json()
        read_mock_metadata_data  = self.read_file("update.json")
        mock_metadata_data = json.loads(read_mock_metadata_data)
        self.assertEqual(mock_metadata_data.keys(), response.keys())

    def test_delete_metadata(self):
        response = self.client.stack(api_key).metadata(metadata_uid).delete().json()
        read_mock_metadata_data  = self.read_file("delete.json")
        mock_metadata_data = json.loads(read_mock_metadata_data)
        self.assertEqual(mock_metadata_data['notice'], response['notice'])
        

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
        response = self.client.stack(api_key).metadata(metadata_uid).publish(data).json()
        self.assertEqual("Metadata sent for publishing.", response['notice'])

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
        response = self.client.stack(api_key).metadata(metadata_uid).unpublish(data).json()
        self.assertEqual("Metadata sent for unpublishing.", response['notice'])
