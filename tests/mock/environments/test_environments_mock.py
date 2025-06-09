import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
environments_name = credentials["environments_name"]


class EnvironmentMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_environments/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_environments(self):
        response = self.client.stack(api_key).environments().find().json()
        read_mock_environments_data  = self.read_file("find.json")
        mock_environments_data = json.loads(read_mock_environments_data)
        self.assertEqual(mock_environments_data.keys(), response.keys())

    def test_get_a_environments(self):
        response = self.client.stack(api_key).environments(environments_name).fetch().json()
        read_mock_environments_data  = self.read_file("fetch.json")
        mock_environments_data = json.loads(read_mock_environments_data)
        self.assertEqual(mock_environments_data.keys(), response.keys())

    def test_create(self):
        data = {
                    "environment": {
                        "name": "test",
                        "urls": [{
                            "locale": "en-us",
                            "url": "http://example.com/"
                        }]
                    }
                }
        response = self.client.stack(api_key).environments().create(data).json()
        read_mock_environments_data  = self.read_file("create.json")
        mock_environments_data = json.loads(read_mock_environments_data)
        self.assertEqual(mock_environments_data.keys(), response.keys())

    def test_update_environments(self):
        data = {
                    "environment": {
                        "name": "test",
                        "urls": [{
                            "locale": "en-us",
                            "url": "http://example.com/"
                        }]
                    }
                }
        response = self.client.stack(api_key).environments(environments_name).update(data).json()
        read_mock_environments_data  = self.read_file("update.json")
        mock_environments_data = json.loads(read_mock_environments_data)
        self.assertEqual(mock_environments_data.keys(), response.keys())

    def test_delete_environments(self):
        response = self.client.stack(api_key).environments(environments_name).delete().json()
        read_mock_environments_data  = self.read_file("delete.json")
        mock_environments_data = json.loads(read_mock_environments_data)
        self.assertEqual(mock_environments_data['notice'], response['notice'])
    