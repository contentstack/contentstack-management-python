import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()
class OrganizationApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

    
    def test_get_organization(self):    
        response = self.client.organizations(os.getenv("org_uid")).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_organizations(self):    
        response = self.client.organizations().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_get_organization_roles(self):    
        response = self.client.organizations(os.getenv('org_uid')).roles()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_organization_add_users(self):  
        data = {
                    "share": {
                        "users": {
                            "abc@sample.com": ["orgAdminRoleUid"],
                            "xyz@sample.com": ["orgMemberRoleUid"]
                        },
                        "stacks": {
                            "abc@sample.com": {
                                "{piKey": ["{{stackRoleUid1}}"]
                            },
                            "xyz@sample.com": {
                                "blta1ed1f11111c1eb1": ["blt111d1b110111e1f1"],
                                "bltf0c00caa0f0000f0": ["bltcea22222d2222222", "blt333f33cb3e33ffde"]
                            }
                        },
                        "message": "Invitation message"
                    }
                }     
        response = self.client.organizations(os.getenv('org_uid')).add_users(json.dumps(data))
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_transfer_organizations_ownership(self):    
        data = {"transfer_to": "abc@sample.com"}
        response= self.client.organizations(os.getenv('org_uid')).transfer_ownership(json.dumps(data))
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_organization_stacks(self):    
        response = self.client.organizations(os.getenv('org_uid')).stacks()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)
    
    def test_organization_logs(self):    
        response = self.client.organizations(os.getenv('org_uid')).logs()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    

if __name__ == '__main__':
    unittest.main()
