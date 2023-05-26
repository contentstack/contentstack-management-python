import unittest
import json
from config2.config import config
from contentstack_management import contentstack


class OrganizationTests(unittest.TestCase):

    def setUp(self):
        config.get_env()
        config.get()
        self.client = contentstack.client(host=config.host.host)
        self.client.login(config.login.email, config.login.password)

    
    def test_organization_get(self):    
        response = self.client.organizations().get() 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, "https://api.contentstack.io/v3/organizations")
        self.assertEqual(response.request.method, "GET")


    def test_get_organization(self):    
        response = self.client.organizations(config.organization.org_uid).get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}")
        self.assertEqual(response.request.method, "GET")

    def test_get_organizations(self):    
        response = self.client.organizations().get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations")
        self.assertEqual(response.request.method, "GET")

    def test_get_organization_roles(self):    
        response = self.client.organizations(config.organization.org_uid).get_organization_roles()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}/roles")
        self.assertEqual(response.request.method, "GET")

    def test_organization_add_users(self):    
        response = self.client.organizations(config.organization.org_uid).organization_add_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}/share")
        self.assertEqual(response.request.method, "GET")

    def test_transfer_organizations_ownership(self):    
        data = {"transfer_to": "abc@sample.com"}
        response= self.client.organizations(config.organization.org_uid).transfer_organizations_ownership(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}/transfer-ownership")
        self.assertEqual(response.request.method, "POST")

    def test_organization_stacks(self):    
        response = self.client.organizations(config.organization.org_uid).organization_stacks()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}/stacks")
        self.assertEqual(response.request.method, "GET")
    
    def test_organization_logs(self):    
        response = self.client.organizations(config.organization.org_uid).organization_logs()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"https://api.contentstack.io/v3/organizations/{config.organization.org_uid}/logs")
        self.assertEqual(response.request.method, "GET")

    

if __name__ == '__main__':
    unittest.main()
