import os
import unittest
import json
from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
asset_uid = credentials["asset_uid"]
folder_uid = credentials["folder_uid"]

def read_file(self, file_name):
	file_path = f"tests/resources/mock_assets/{file_name}"
	infile = open(file_path, 'r')
	data = infile.read()
	infile.close()
	return data

class AssetsMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_get_all_assets(self):
        response = self.client.stack(api_key).assets().find().json()
        read_mock_asset_data = read_file("find.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_get_asset(self):
        response = self.client.stack(api_key).assets(asset_uid).fetch().json()
        self.assertEqual(asset_uid, response["assets"]["uid"])

    def test_delete(self):
        response = self.client.stack(api_key).assets(asset_uid).delete().json()
        self.assertEqual("Asset deleted successfully.", response['notice'])

    def test_specific_folder(self):
        response = self.client.stack(api_key).assets().specific_folder(folder_uid).json()
        self.assertEqual(asset_uid, response["assets"]["uid"])

    def test_subfolder(self):
        response = self.client.stack(api_key).assets().subfolders(folder_uid).json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(asset_uid, response["assets"]["uid"])

    def test_upload(self):
        file_path = f"tests/mock/resources/mock_assets/image.jpg"
        response = self.client.stack(api_key).assets().upload(file_path).json()
        self.assertEqual("Asset created successfully.", response['notice'])

    def test_replace(self):
        file_path = f"tests/mock/resources/mock_assets/image.jpg"
        response = self.client.stack(api_key).assets(asset_uid).replace(file_path).json()
        self.assertEqual("Asset updated successfully.", response['notice'])

    def test_generate(self):
        data = {
                "asset": {
                    "permanent_url": "https://images.contentstack.io/v3/assets/stack_api_key/asset_UID/sample-slug.jpeg"
                    }
                }
        response = self.client.stack(api_key).assets(asset_uid).generate(data).json()
        self.assertEqual("Asset updated successfully.", response['notice'])

    def test_download(self):
        response = self.client.stack(api_key).assets(asset_uid).download().json()
        self.assertEqual(response.status_code, 200)

    def test_rte(self):
        response = self.client.stack().assets().rte().json()
        read_mock_asset_data = read_file("rte.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_version_naming(self):
        version_number = 1
        data = {
	        "upload": {
		    "_version_name": "Version name"
	        }
        }
        response = self.client.stack().assets(asset_uid).version_naming(version_number, data).json()
        self.assertEqual("Version name assigned successfully.", response['notice'])

    def test_version(self):
        response = self.client.stack().assets(asset_uid).version().json()
        read_mock_asset_data = read_file("version.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_delete_version(self):
        version_number = 1
        response = self.client.stack().assets(asset_uid).version_delete(version_number).json()
        self.assertEqual("Version name deleted successfully.", response['notice'])

    def test_references(self):
        response = self.client.stack().assets(asset_uid).references().json()
        read_mock_asset_data = read_file("references.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_asset_type(self):
        asset_type = "images"
        response = self.client.stack().assets().specific_asset_type(asset_type).json()
        read_mock_asset_data = read_file("assset_type.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_update_asset_revision(self):
        data = {
	        "asset": {
		        "title": "Title",
		        "description": "Description"
	        },
	        "version": 2
        }
        response = self.client.stack().assets(asset_uid).update_asset_revision(data).json()
        self.assertEqual("Asset updated successfully.", response['notice'])

    def test_update(self):
        data = {
	        "asset": {
		        "title": "Title"
	        }
        }
        response = self.client.stack().assets(asset_uid).update_asset_revision(data).json()
        self.assertEqual("Asset updated successfully.", response['notice'])

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
        response = self.client.stack().assets(asset_uid).publish(data).json()
        self.assertEqual("Asset sent for publishing.", response['notice'])

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
        response = self.client.stack().assets(asset_uid).unpublish(data).json()
        self.assertEqual("Asset sent for unpublishing.", response['notice'])

    def test_get_folder(self):
        response = self.client.stack().assets().folder_collection(folder_uid).json()
        read_mock_asset_data = read_file("folder.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())
        

    def test_get_folder_by_name(self):
        query = {"is_dir": True, "name": "folder_name"}
        response = self.client.stack().assets().folder_collection(query).json()
        read_mock_asset_data = read_file("folder.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_get_subfolder(self):
        query = {"is_dir": True}
        response = self.client.stack().assets().folder_collection(folder_uid, query).json()
        read_mock_asset_data = read_file("folder.json")
        mock_asset_data = json.loads(read_mock_asset_data)
        self.assertEqual(mock_asset_data.keys(), response.keys())

    def test_create_folder(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack().assets().create_folder(data).json()
        self.assertEqual("Folder created successfully.", response['notice'])

    def test_update_or_move(self):
        data = {
	        "asset": {
		        "name": "Demo"
	        }
        }
        response = self.client.stack().assets().update_or_move(folder_uid, data).json()
        self.assertEqual("Folder updated successfully.", response['notice'])

    def test_delete_folder(self):
        response = self.client.stack().assets().delete_folder(folder_uid).json()
        self.assertEqual("Folder deleted successfully.", response['notice'])