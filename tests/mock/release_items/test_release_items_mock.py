import os
import json
import unittest
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
releases_uid = credentials["release_uid"]

class ReleaseItemsMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def read_file(self, file_name):
        file_path= f"tests/resources/mock_release_items/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_get_all_item(self):
        response = self.client.stack(api_key).releases(releases_uid).item().find().json()
        read_mock_releases_data  = self.read_file("find.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())
        
    def test_create(self):
        data = {
                "item": {
                    "version": 1,
                    "uid": "entry_or_asset_uid",
                    "content_type_uid": "demo1",
                    "action": "publish",
                    "locale": "en-us"
                }
            }
        response = self.client.stack(api_key).releases(releases_uid).item().create(data).json()
        read_mock_releases_data  = self.read_file("create.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_create_multiple(self):
        data = {
                "items": [{
                    "uid": "entry_or_asset_uid1",
                    "version": 1,
                    "locale": "en-us",
                    "content_type_uid": "demo1",
                    "action": "publish"
                }, {
                    "uid": "entry_or_asset_uid2",
                    "version": 4,
                    "locale": "fr-fr",
                    "content_type_uid": "demo2",
                    "action": "publish"
                }]
            }
        response = self.client.stack(api_key).releases(releases_uid).item().create_multiple(data).json()
        read_mock_releases_data  = self.read_file("create_multiple.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())


    def test_update(self):
        data = {
                "items":[
                    "$all"
                ]
            }
        response = self.client.stack(api_key).releases(releases_uid).item().update(data).json()
        read_mock_releases_data  = self.read_file("update.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_delete(self):
        data = {
                "items": [{
                    "uid": "item_uid",
                    "version": 1,
                    "locale": "ja-jp",
                    "content_type_uid": "category",
                    "action": "publish"
                }]
            }
        response = self.client.stack(api_key).releases(releases_uid).item().delete(data).json()
        read_mock_releases_data  = self.read_file("delete.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_delete_multiple(self):
        data = {
                "items": [{
                    "uid": "item_uid",
                    "locale": "en-us",
                    "version": 1,
                    "content_type_uid": "your_content_type_uid",
                    "action": "publish_or_unpublish"
                }]
            }
        response = self.client.stack(api_key).releases(releases_uid).item().delete_multiple(data).json()
        read_mock_releases_data  = self.read_file("delete.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())
    
    


    