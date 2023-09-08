import json
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


class OrganizationApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)
        self.organization = self.client.organizations(organization_uid)

    def test_get_organization(self):
        response = self.organization.fetch()
        assert response.request.method == "GET"
        assert response.request.url == 'https://api.contentstack.io/v3/organizations/orgcontentstack'
        assert response.request.headers["Content-Type"] == "application/json"
        assert response.request.body is None

    def test_get_organizations(self):
        response = self.client.organizations().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 401)

    def test_get_organization_roles(self):
        response = self.organization.roles()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

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
        response = self.organization.add_users(json.dumps(data))
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_transfer_organizations_ownership(self):
        data = {"transfer_to": "abc@sample.com"}
        response = self.organization.transfer_ownership(json.dumps(data))
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_organization_stacks(self):
        response = self.organization.stacks()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_organization_logs(self):
        response = self.organization.logs()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
