import unittest
import json
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
global_field_uid = credentials["global_field_uid"]

class GlobalFieldsApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)
     
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_global_fields/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_fetch_global_fields(self):    
        response = self.client.stack(api_key).global_fields(global_field_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_find_all_global_fields(self):    
        response = self.client.stack(api_key).global_fields().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_create_global_fields(self): 
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)
        response = self.client.stack(api_key).global_fields().create(read_mock_global_fileds_data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_update_global_fields(self):
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)    
        response = self.client.stack(api_key).global_fields(global_field_uid).update(read_mock_global_fileds_data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    def test_delete_global_fields(self):    
        response= self.client.stack(api_key).global_fields(global_field_uid).delete()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    def test_import_global_fields(self):
        file_path = "tests/resources/mock_global_fields/import_global_fields.json"
        response = self.client.stack(api_key).global_fields().imports(file_path)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)
    
    def test_export_global_fields(self):    
        response = self.client.stack(api_key).global_fields(global_field_uid).export()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    

if __name__ == '__main__':
    unittest.main()
