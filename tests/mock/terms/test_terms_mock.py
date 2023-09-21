import os
import json
import unittest
from dotenv import load_dotenv
from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
taxonomy_uid = credentials["taxonomy_uid"]
terms_uid = credentials["terms_uid"]
terms_string = credentials["terms_string"]

class TermsMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def read_file(self, file_name):
        file_path= f"tests/resources/mock_terms/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_get_all_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().find().json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_get_a_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).fetch().json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())
        
    def test_create(self):
        data = {
                "term": {
                    "uid": "term_192",
                    "name": "Term 192",
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().create(data).json()
        read_mock_taxonomy_data  = self.read_file("create.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())


    def test_update(self):
        data = {
                "term": {
                    "name": "Term 190"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).update(data).json()
        read_mock_taxonomy_data  = self.read_file("update.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_delete(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).delete().json()
        read_mock_taxonomy_data  = self.read_file("fetch.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())


    def test_search(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().search(terms_string).json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_move(self):
        data = {
                "term": {
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).move(data).json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    def test_ancestors(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).ancestors().json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

    
    def test_descendants(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).descendants().json()
        read_mock_taxonomy_data  = self.read_file("find.json")
        mock_taxonomy_data = json.loads(read_mock_taxonomy_data)
        self.assertEqual(mock_taxonomy_data.keys(), response.keys())

if __name__ == '__main__':
    unittest.main()
