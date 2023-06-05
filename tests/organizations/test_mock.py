import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()
class OrganizationTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

    def read_file(self, file_name):
        file_path= f"tests/resources/mockorg/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    
    def test_organization_get(self):    
        response = self.client.organizations().get().json()
        read_mock_org_data = self.read_file("get_all.json")
        mock_org_data = json.loads(read_mock_org_data)
        self.assertEqual(mock_org_data.keys(), response.keys())
        


    def test_get_organization(self):    
        response = self.client.organizations(os.getenv("org_uid")).get().json()
        self.assertEqual(os.getenv("org_uid"), response["organization"]["uid"])
        

    def test_get_organizations(self):    
        response = self.client.organizations().get().json()
        read_mock_org_data = self.read_file("get_all.json")
        mock_org_data = json.loads(read_mock_org_data)
        self.assertEqual(mock_org_data.keys(), response.keys())

    def test_get_organization_roles(self):    
        response = self.client.organizations(os.getenv('org_uid')).get_organization_roles().json()
        self.assertEqual(os.getenv("org_uid"), response["roles"][0]["org_uid"])

    def test_organization_add_users(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_add_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/share")
        self.assertEqual(response.request.method, "GET")

    def test_transfer_organizations_ownership(self):    
        data = {"transfer_to": "abc@sample.com"}
        response= self.client.organizations(os.getenv('org_uid')).transfer_organizations_ownership(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/transfer-ownership")
        self.assertEqual(response.request.method, "POST")

    def test_organization_stacks(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_stacks()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/stacks")
        self.assertEqual(response.request.method, "GET")
    
    def test_organization_logs(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_logs()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/logs")
        self.assertEqual(response.request.method, "GET")

    

if __name__ == '__main__':
    unittest.main()
