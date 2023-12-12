import json
import os
import unittest

from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
organization_uid = credentials["organization_uid"]

class OrganizationMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def read_file(self, file_name):
        file_path = f"tests/resources/mockorg/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_organization_get(self):
        response = self.client.organizations().find().json()
        read_mock_org_data = self.read_file("get_all.json")
        mock_org_data = json.loads(read_mock_org_data)
        self.assertEqual(mock_org_data.keys(), response.keys())

    def test_get_organization(self):
        response = self.client.organizations(organization_uid).fetch().json()
        self.assertEqual(organization_uid, response["organization"]["uid"])

    def test_get_organizations(self):
        response = self.client.organizations().find().json()
        read_mock_org_data = self.read_file("get_all.json")
        mock_org_data = json.loads(read_mock_org_data)
        self.assertEqual(mock_org_data.keys(), response.keys())

    def test_get_organization_roles(self):
        response = self.client.organizations(organization_uid).roles().json()
        self.assertEqual(organization_uid, response["roles"][0]["org_uid"])

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
        response = self.client.organizations(organization_uid).add_users(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/share")
        self.assertEqual(response.request.method, "POST")

    def test_transfer_organizations_ownership(self):
        data = {"transfer_to": "abc@sample.com"}
        response = self.client.organizations(organization_uid).transfer_ownership(json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}organizations/{organization_uid}/transfer-ownership")
        self.assertEqual(response.request.method, "POST")

    def test_organization_stacks(self):
        response = self.client.organizations(organization_uid).stacks()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/stacks")
        self.assertEqual(response.request.method, "GET")

    def test_organization_logs(self):
        response = self.client.organizations(organization_uid).logs()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}organizations/{organization_uid}/logs")
        self.assertEqual(response.request.method, "GET")


if __name__ == '__main__':
    unittest.main()
