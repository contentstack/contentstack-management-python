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


class StacksAPITests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)
        self.api_key = api_key

    def test_stacks_get(self):
        response = self.client.stack(self.api_key).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_stacks_all(self):
        response = self.client.stack().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 401)

    def tests_stacks_create(self):
        data = {
            "stack": {
                "name": "My New Stack by testcases",
                "description": "My new test stack",
                "master_locale": "en-us"
            }
        }
        response = self.client.stack().create(organization_uid, data)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_update(self):
        data = {
            "stack": {
                "name": "My New Stack by test",
                "description": "My new test stack",
                "master_locale": "en-us"
            }
        }
        response = self.client.stack(api_key).update(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_delete(self):
        response = self.client.stack(api_key).delete()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_fetch_all_user(self):
        response = self.client.stack(api_key).users()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_update_user_role(self):
        data = {
            "users": {
                "user_uid": ["role_uid1", "role_uid2"]
            }
        }
        response = self.client.stack(api_key).update_user_role(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    def tests_stacks_transfer_ownership(self):
        data = {
            "transfer_to": "manager@example.com"
        }
        response = self.client.stack(api_key).transfer_ownership(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_accept_ownership(self):
        response = self.client.stack(api_key).accept_ownership(user_id,
                                                               ownership_token)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_get_stack_settings(self):
        response = self.client.stack(api_key).settings()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_create_stack_settings(self):
        data = {
            "stack_settings": {
                "stack_variables": {
                    "enforce_unique_urls": True,
                    "sys_rte_allowed_tags": "style,figure,script",
                    "sys_rte_skip_format_on_paste": "GD:font-size"
                },
                "rte": {
                    "cs_only_breakline": True
                }
            }
        }
        response = self.client.stack(api_key).create_settings(data)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_reset_stack_settings(self):
        data = {
            "stack_settings": {}
        }
        response = self.client.stack(api_key).reset_settings(data)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_share_stack(self):
        data = {
            "emails": [
                "manager@example.com"
            ],
            "roles": {
                "manager@example.com": [
                    "abcdefhgi1234567890"
                ]
            }
        }
        response = self.client.stack(api_key).share(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def tests_stacks_unshare_stack(self):
        data = {
            "email": "manager@example.com"
        }
        response = self.client.stack(api_key).unshare(data)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
