import json
import os
import unittest

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
organization_uid = credentials["organization_uid"]
user_id = credentials["user_id"]
ownership_token = credentials["ownership_token"]


class OrganizationUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(os.getenv("email"), os.getenv("password"))

    def test_fetch_organization(self):
        response = self.client.organizations(os.getenv("org_uid")).fetch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}")
        self.assertEqual(response.request.method, "GET")

    def test_find_organizations(self):
        response = self.client.organizations().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations")
        self.assertEqual(response.request.method, "GET")

    def test_get_organization_roles(self):
        response = self.client.organizations(os.getenv('org_uid')).roles()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/roles")
        self.assertEqual(response.request.method, "GET")

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
                        "a": [""],
                        "b": ["", ""]
                    }
                },
                "message": "Invitation message"
            }
        }
        response = self.client.organizations(os.getenv('org_uid')).add_users(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/share")
        self.assertEqual(response.request.method, "POST")

    def test_transfer_organizations_ownership(self):
        data = {"transfer_to": "abc@sample.com"}
        response = self.client.organizations(os.getenv('org_uid')).transfer_ownership(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/transfer-ownership")
        self.assertEqual(response.request.method, "POST")

    def test_organization_stacks(self):
        response = self.client.organizations(os.getenv('org_uid')).stacks()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/stacks")
        self.assertEqual(response.request.method, "GET")

    def test_organization_logs(self):
        response = self.client.organizations(os.getenv('org_uid')).logs()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/organizations/{os.getenv('org_uid')}/logs")
        self.assertEqual(response.request.method, "GET")


if __name__ == '__main__':
    unittest.main()
