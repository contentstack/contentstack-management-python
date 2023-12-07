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
releases_uid = credentials["release_uid"]

class ReleaseItemsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_item(self):
        response = self.client.stack(api_key).releases(releases_uid).item().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/items")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)
        
    def test_create_item(self):
        data = {
                "item": {
                    "version": 1,
                    "uid": "entry_or_asset_uid",
                    "content_type_uid": "your_content_type_uid",
                    "action": "publish",
                    "locale": "en-us"
                }
            }
        response = self.client.stack(api_key).releases(releases_uid).item().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/item")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_create_multiple_item(self):
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
        response = self.client.stack(api_key).releases(releases_uid).item().create_multiple(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/items")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_update(self):
        data = {
                "term": {
                    "name": "Term 1"
                }
                }
        response = self.client.stack(api_key).releases(releases_uid).item().update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/update_items")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete(self):
        data = {
                "items": [{
                    "uid": "items_uid",
                    "version": 1,
                    "locale": "ja-jp",
                    "content_type_uid": "category",
                    "action": "publish"
                }]
            }
        response = self.client.stack(api_key).releases(releases_uid).item().delete(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/items")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


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
        response = self.client.stack(api_key).releases(releases_uid).item().delete_multiple(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{releases_uid}/items?all=True")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


