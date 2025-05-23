import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
asset_uid = credentials["asset_uid"]
folder_uid = credentials["folder_uid"]

class AssetsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_assets(self):
        response = self.client.stack(api_key).assets().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_asset(self):
        response = self.client.stack(api_key).assets(asset_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_delete(self):
        response = self.client.stack(api_key).assets(asset_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_specific_folder(self):
        response = self.client.stack(api_key).assets().specific_folder(folder_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets?folder={folder_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_subfolder(self):
        response = self.client.stack(api_key).assets().subfolders(folder_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets?include_folders=True&folder={folder_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_upload(self):
        file_path = "tests/resources/mock_assets/chaat.jpeg"
        response = self.client.stack(api_key).assets().upload(file_path)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets")
        self.assertEqual(response.request.method, "POST")

    def test_replace(self):
        file_path = "tests/resources/mock_assets/chaat.jpeg"
        response = self.client.stack(api_key).assets(asset_uid).replace(file_path)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "PUT")

    def test_generate(self):
        data = {
                "asset": {
                    "permanent_url": "https://images.contentstack.io/v3/assets/stack_api_key/asset_UID/sample-slug.jpeg"
                    }
                }
        response = self.client.stack(api_key).assets(asset_uid).generate(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_download(self):
        response = self.client.stack(api_key).assets(asset_uid).download()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{api_key}/{asset_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_rte(self):
        response = self.client.stack(api_key).assets().rte()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/rt")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.body, None)

    def test_version_naming(self):
        version_number = 1
        data = {
	        "upload": {
		    "_version_name": "Version name"
	        }
        }
        response = self.client.stack(api_key).assets(asset_uid).version_naming(version_number, data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/versions/{version_number}/name")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_version(self):
        response = self.client.stack(api_key).assets(asset_uid).version()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/versions")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_delete_version(self):
        version_number = 1
        response = self.client.stack(api_key).assets(asset_uid).version_delete(version_number)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/versions/{version_number}/name")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_references(self):
        response = self.client.stack(api_key).assets(asset_uid).references()
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/references")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_asset_type(self):
        asset_type = "images"
        response = self.client.stack(api_key).assets().specific_asset_type(asset_type)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_type}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_update_asset_revision(self):
        data = {
	        "asset": {
		        "title": "Title",
		        "description": "Description"
	        },
	        "version": 2
        }
        response = self.client.stack(api_key).assets(asset_uid).update_asset_revision(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update(self):
        data = {
	        "asset": {
		        "title": "Title"
	        }
        }
        response = self.client.stack(api_key).assets(asset_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "multipart/form-data")

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
        response = self.client.stack(api_key).assets(asset_uid).publish(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/publish")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

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
        response = self.client.stack(api_key).assets(asset_uid).unpublish(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/{asset_uid}/unpublish")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_get_folder(self):
        response = self.client.stack(api_key).assets().folder(folder_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/folders/{folder_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_folder_by_name(self):
        response = self.client.stack(api_key).assets().folder_by_name()
        p=print(response.request.url)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets?query=is_dir&query=name")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_subfolders(self):
        response = self.client.stack(api_key).assets().get_subfolders(folder_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets?include_folders=True&query=is_dir&folder={folder_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_folder(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack(api_key).assets().create_folder(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/folders")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_or_move(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack(api_key).assets().update_or_move(folder_uid, data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/folders/{folder_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_folder(self):
        response = self.client.stack(api_key).assets().delete_folder(folder_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}assets/folders/{folder_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")