import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()
class GlobalFieldsApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))
     
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_global_fields/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_fetch_global_fields(self):    
        response = self.client.stack(os.getenv('api_key')).global_fields(os.getenv("global_field_uid")).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_fetch_all_global_fields(self):    
        response = self.client.stack(os.getenv('api_key')).global_fields().fetch_all()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_create_global_fields(self): 
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)
        response = self.client.stack(os.getenv('api_key')).global_fields().create(read_mock_global_fileds_data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_update_global_fields(self):
        read_mock_global_fileds_data = self.read_file("create_global_fields.json")
        read_mock_global_fileds_data = json.loads(read_mock_global_fileds_data)    
        response = self.client.stack(os.getenv('api_key')).global_fields(os.getenv('global_field_uid')).update(read_mock_global_fileds_data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_delete_global_fields(self):    
        response= self.client.stack(os.getenv('api_key')).global_fields(os.getenv('global_field_uid')).delete()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_import_global_fields(self):
        file_path = "tests/resources/mock_global_fields/import_global_fields.json"
        response = self.client.stack(os.getenv('api_key')).global_fields().import_global_fields(file_path)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)
    
    def test_export_global_fields(self):    
        response = self.client.stack(os.getenv('api_key')).global_fields(os.getenv('global_field_uid')).export()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    

if __name__ == '__main__':
    unittest.main()
