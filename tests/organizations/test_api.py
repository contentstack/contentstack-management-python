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

    
    def test_organization_get(self):    
        response = self.client.organizations().get() 
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)


    def test_get_organization(self):    
        response = self.client.organizations(os.getenv("org_uid")).get()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_organizations(self):    
        response = self.client.organizations().get()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_organization_roles(self):    
        response = self.client.organizations(os.getenv('org_uid')).get_organization_roles()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_organization_add_users(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_add_users()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_transfer_organizations_ownership(self):    
        data = {"transfer_to": "abc@sample.com"}
        response= self.client.organizations(os.getenv('org_uid')).transfer_organizations_ownership(json.dumps(data))
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_organization_stacks(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_stacks()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)
    
    def test_organization_logs(self):    
        response = self.client.organizations(os.getenv('org_uid')).organization_logs()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    

if __name__ == '__main__':
    unittest.main()
