import json
import os
import unittest

import contentstack_management
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
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_fetch_organization(self):
        response = self.client.organizations(organization_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_organizations(self):
        response = self.client.organizations().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_organization_roles(self):
        response = self.client.organizations(organization_uid).roles()
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/roles")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

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
        response = self.client.organizations(organization_uid).add_users(json.dumps(data))
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/share")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_transfer_organizations_ownership(self):
        data = {"transfer_to": "abc@sample.com"}
        response = self.client.organizations(organization_uid).transfer_ownership(json.dumps(data))
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}organizations/{organization_uid}/transfer-ownership")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_organization_stacks(self):
        response = self.client.organizations(organization_uid).stacks()
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/stacks")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_organization_logs(self):
        response = self.client.organizations(organization_uid).logs()
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/logs")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)


if __name__ == '__main__':
    unittest.main()
