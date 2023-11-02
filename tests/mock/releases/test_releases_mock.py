import json
import os
import unittest

from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
release_uid = credentials["release_uid"]


class ReleasesMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_releases/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_releases(self):
        response = self.client.stack(api_key).releases().find().json()
        read_mock_releases_data  = self.read_file("find.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_get_a_releases(self):
        response = self.client.stack(api_key).releases(release_uid).fetch().json()
        read_mock_releases_data  = self.read_file("fetch.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_create(self):
        data = {
                "release": {
                    "name": "Release Name",
                    "description": "2018-12-12",
                    "locked": False,
                    "archived": False
                }
            }

        response = self.client.stack(api_key).releases().create(data).json()
        read_mock_releases_data  = self.read_file("create.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_update_releases(self):
        data = {
            "release": {
                "name": "Release Name",
                "description": "2018-12-22"
            }
        }
        response = self.client.stack(api_key).releases(release_uid).update(data).json()
        read_mock_releases_data  = self.read_file("update.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())

    def test_delete_releases(self):
        response = self.client.stack(api_key).releases(release_uid).delete().json()
        read_mock_releases_data  = self.read_file("delete.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data['notice'], response['notice'])

    def test_clone(self):
        data = {
                "release": {
                    "name": "New Release Name",
                    "description": "2018-12-12"
                }
            }

        response = self.client.stack(api_key).releases(release_uid).clone(data).json()
        read_mock_releases_data  = self.read_file("clone.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())


    def test_deploy(self):
        data = {
                "release": {
                    "environments": [
                        "development"
                    ]
                }
            }

        response = self.client.stack(api_key).releases(release_uid).deploy(data).json()
        read_mock_releases_data  = self.read_file("deploy.json")
        mock_releases_data = json.loads(read_mock_releases_data)
        self.assertEqual(mock_releases_data.keys(), response.keys())
        
