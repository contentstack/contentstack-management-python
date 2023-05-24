import unittest
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
        self.assertEqual(response.request.url, "https://eu-api.contentstack.com/v3/organizations")
        self.assertEqual(response.request.method, "get")


    def test_get_organization(self):    
        response = self.client.organizations().get_organization(config.organization.org_uid)
        self.assertEqual(response.status_code, 200)

    def test_get_organization_roles(self):    
        response = self.client.organizations().get_organization_roles(config.organization.org_uid)
        self.assertEqual(response.status_code, 200)

    def test_organization_add_users(self):    
        response = self.client.organizations().organization_add_users(config.organization.org_uid)
        self.assertEqual(response.status_code, 200)

    def test_transfer_organizations_ownership(self):    
        data = {
            "transfer_to": "abc@sample.com"
        }
        response= self.client.organizations().transfer_organizations_ownership('blt49fccf494fadf141',data)
        self.assertEqual(response.status_code, 400)

    def test_organization_stacks(self):    
        response = self.client.organizations().organization_stacks(config.organization.org_uid)
        self.assertEqual(response.status_code, 200)

    

if __name__ == '__main__':
    unittest.main()
