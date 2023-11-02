import unittest
import json
import os
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
global_field_uid = credentials["global_field_uid"]

class GlobalFieldsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username,password)
    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_global_fields/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_global_field(self):    
        response = self.client.stack(api_key).global_fields(global_field_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields/{global_field_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_all_global_fields(self):    
        response = self.client.stack(api_key).global_fields().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_global_fields(self): 
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)
        response = self.client.stack(api_key).global_fields().create(read_mock_global_fileds_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_global_fields(self):
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)    
        response = self.client.stack(api_key).global_fields(global_field_uid).update(read_mock_global_fileds_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields/{global_field_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_global_fields(self):    
        response= self.client.stack(api_key).global_fields(global_field_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields/{global_field_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_import_global_fields(self):
        file_path = "tests/resources/mock_global_fields/import_global_fields.json"
        response = self.client.stack(api_key).global_fields().imports(file_path)
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields/import")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "multipart/form-data")
    
    def test_export_global_fields(self):    
        response = self.client.stack(api_key).global_fields(global_field_uid).export()
        self.assertEqual(response.request.url, f"{self.client.endpoint}global_fields/{global_field_uid}/export")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    

if __name__ == '__main__':
    unittest.main()
