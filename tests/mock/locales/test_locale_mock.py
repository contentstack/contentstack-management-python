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
locale_code = credentials["locale_code"]


class LocaleMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_locales/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_locale(self):
        response = self.client.stack(api_key).locale().find().json()
        read_mock_locale_data  = self.read_file("find.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())

    def test_get_a_locale(self):
        response = self.client.stack(api_key).locale(locale_code).fetch().json()
        read_mock_locale_data  = self.read_file("fetch.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())

    def test_create(self):
        data = {
                "locale": {
                    "name": "Tamil",
                    "code": "TA",
                    "fallback_locale": "en-us"
                    }
                }
        response = self.client.stack(api_key).locale().create(data).json()
        read_mock_locale_data  = self.read_file("create.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())

    def test_update_locale(self):
        data = {
                "locale":{
                    "name":"Tamilu",
                    "fallback_locale":"en-at"
                }
                }
        response = self.client.stack(api_key).locale(locale_code).update(data).json()
        read_mock_locale_data  = self.read_file("update.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())

    def test_delete_locale(self):
        response = self.client.stack(api_key).locale(locale_code).delete().json()
        read_mock_locale_data  = self.read_file("delete.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data['notice'], response['notice'])
        

    def test_set_fallback(self):
        data = {
                "locale": {
                    "name": "Kannada",
                    "code": "KA",
                    "fallback_locale": "en-us"
                }
                }
        response = self.client.stack(api_key).locale().set_fallback(data).json()
        read_mock_locale_data  = self.read_file("create.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())

    def test_update_fallback(self):
        data = {
                "locale": {
                    "name": "Kannada",
                    "code": "KA",
                    "fallback_locale": "en-us"
                    }
                }
        response = self.client.stack(api_key).locale(locale_code).update_fallback(data).json()
        read_mock_locale_data  = self.read_file("update.json")
        mock_locale_data = json.loads(read_mock_locale_data)
        self.assertEqual(mock_locale_data.keys(), response.keys())