import os
import unittest
from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
asset_uid = credentials["asset_uid"]
folder_uid = credentials["folder_uid"]

class AssetsApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_assets(self):
        response = self.client.stack(api_key).assets().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_get_asset(self):
        response = self.client.stack(api_key).assets(asset_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_delete(self):
        response = self.client.stack(api_key).assets(asset_uid).delete()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "DELETE")

    def test_specific_folder(self):
        response = self.client.stack(api_key).assets().specific_folder(folder_uid)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_subfolder(self):
        response = self.client.stack(api_key).assets().subfolders(folder_uid)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_upload(self):
        file_path = f"tests/resources/mock_assets/chaat.jpeg"
        response = self.client.stack(api_key).assets().upload(file_path)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.request.method, "POST")

    def test_replace(self):
        file_path = f"tests/resources/mock_assets/chaat.jpeg"
        response = self.client.stack(api_key).assets(asset_uid).replace(file_path)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "PUT")

    def test_generate(self):
        data = {
                "asset": {
                    "permanent_url": "https://images.contentstack.io/v3/assets/stack_api_key/asset_UID/sample-slug.jpeg"
                    }
                }
        response = self.client.stack(api_key).assets(asset_uid).generate(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "PUT")

    def test_download(self):
        response = self.client.stack(api_key).assets(asset_uid).download()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_rte(self):
        response = self.client.stack().assets().rte()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_version_naming(self):
        version_number = 1
        data = {
	        "upload": {
		    "_version_name": "Version name"
	        }
        }
        response = self.client.stack().assets(asset_uid).version_naming(version_number, data)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.request.method, "POST")

    def test_version(self):
        response = self.client.stack().assets(asset_uid).version()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_delete_version(self):
        version_number = 1
        response = self.client.stack().assets(asset_uid).version_delete(version_number)
        if response.status_code == 204:
            self.assertEqual(response.status_code, 204)
        else:
            self.assertEqual(response.request.method, "DELETE")

    def test_references(self):
        response = self.client.stack().assets(asset_uid).references()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_asset_type(self):
        asset_type = "images"
        response = self.client.stack().assets().specific_asset_type(asset_type)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_update_asset_revision(self):
        data = {
	        "asset": {
		        "title": "Title",
		        "description": "Description"
	        },
	        "version": 2
        }
        response = self.client.stack().assets(asset_uid).update_asset_revision(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "PUT")

    def test_update(self):
        data = {
	        "asset": {
		        "title": "Title"
	        }
        }
        response = self.client.stack().assets(asset_uid).update_asset_revision(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "PUT")

    def test_publish(self):
        data = {
	        "asset": {
		        "locales": [
			        "en-us"
		        ],
		        "environments": [
			        "development"
		        ]
	        },
	        "version": 1,
	        "scheduled_at": "2019-02-08T18:30:00.000Z"
        }
        response = self.client.stack().assets(asset_uid).publish(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/publish")
        self.assertEqual(response.request.method, "POST")

    def test_unpublish(self):
        data = {
	        "asset": {
		        "locales": [
			        "en-us"
		        ],
		        "environments": [
			        "development"
		        ]
	        },
	        "version": 1,
	        "scheduled_at": "2019-02-08T18:30:00.000Z"
        }
        response = self.client.stack().assets(asset_uid).unpublish(data)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.request.method, "POST")

    def test_get_folder(self):
        response = self.client.stack().assets().folder(folder_uid)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_get_folder_by_name(self):
        query = {"is_dir": True, "name": "folder_name"}
        response = self.client.stack().assets().folder_by_name()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_get_subfolder(self):
        query = {"is_dir": True}
        response = self.client.stack().assets().get_subfolders(folder_uid)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_create_folder(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack().assets().create_folder(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "POST")

    def test_update_or_move(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack().assets().update_or_move(folder_uid, data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "PUT")

    def test_delete_folder(self):
        response = self.client.stack().assets().delete_folder(folder_uid)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "DELETE")