import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class StacksTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))
        self.api_key = os.getenv("api_key")

    
    def test_stacks_get(self):    
        response = self.client.stack(self.api_key).fetch() 
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "GET")


    def test_stacks_all(self):    
        response = self.client.stack().all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "GET")

    def tests_stacks_create(self):
        data = {
                "stack": {
                    "name": "My New Stack by testcases",
                    "description": "My new test stack",
                    "master_locale": "en-us"
                }
                }
        response= self.client.stack().create(os.getenv("org_uid"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "POST")
    
    def tests_stacks_update(self):
        data = {
                "stack": {
                    "name": "My New Stack by test",
                    "description": "My new test stack",
                    "master_locale": "en-us"
                }
                }
        response= self.client.stack(os.getenv("api_key")).update(data)
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "PUT")

    def tests_stacks_delete(self):
        response= self.client.stack(os.getenv("api_key")).delete()
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "DELETE")

if __name__ == '__main__':
    unittest.main()
