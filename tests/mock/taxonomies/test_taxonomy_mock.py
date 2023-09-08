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
taxonomy_uid = credentials["taxonomy_uid"]


class TaxonomyMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)
    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_taxonomy/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_taxonomy(self):
        response = self.client.stack(api_key).taxonomy().find().json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_get_a_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).fetch().json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_create(self):
        data = {
                "taxonomy": {
                    "uid": "taxonomy12345",
                    "name": "Taxonomy 12345",
                    "description": "Description for Taxonomy 1"
                }
                }

        response = self.client.stack(api_key).taxonomy().create(data).json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_update_taxonomy(self):
        data = {
                "taxonomy": {
                    "name": "Taxonomy 12345",
                    "description": "Description updated for Taxonomy 12345"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).update(data).json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_delete_taxonomy(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).delete().json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data['notice'], response['notice'])
        
