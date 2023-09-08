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


class StacksUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)
        self.api_key = api_key
        self.stack = self.client.stack(api_key)

    def test_stacks_get(self):
        response = self.stack.fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_stacks_all(self):
        response = self.client.stack().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def tests_stacks_create(self):
        data = {
            "stack": {
                "name": "My New Stack by testcases1",
                "description": "My new test stack",
                "master_locale": "en-us"
            }
        }
        response = self.client.stack().create(organization_uid, data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_update(self):
        data = {
            "stack": {
                "name": "My New Stack by test",
                "description": "My new test stack",
                "master_locale": "en-us"
            }
        }
        response = self.stack.update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_delete(self):
        response = self.stack.delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_fetch_all_user(self):
        response = self.stack.users()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/users")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def tests_stacks_update_user_role(self):
        data = {
            "users": {
                "user_uid": ["role_uid1", "role_uid2"]
            }
        }
        response = self.stack.update_user_role(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/users/roles")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_transfer_ownership(self):
        data = {
            "transfer_to": "manager@example.com"
        }
        response = self.stack.transfer_ownership(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/transfer_ownership")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_accept_ownership(self):
        response = self.stack.accept_ownership(user_id,
                                               ownership_token)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}stacks/accept_ownership/ownership@contentstack?api_key=apikeycontentstack&uid=userid%40contentstack")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def tests_stacks_get_stack_settings(self):
        response = self.stack.settings()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/settings")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def tests_stacks_create_stack_settings(self):
        data = {
            "stack_settings": {
                "stack_variables": {
                    "enforce_unique_urls": True,
                    "sys_rte_allowed_tags": "style,figure,script",
                    "sys_rte_skip_format_on_paste": "GD:font-size"
                },
                "rte": {
                    "cs_only_break line": True
                }
            }
        }
        response = self.stack.create_settings(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/settings")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_reset_stack_settings(self):
        data = {
            "stack_settings": {}
        }
        response = self.stack.reset_settings(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/settings/reset")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

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
        response = self.stack.share(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/share")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def tests_stacks_unshare_stack(self):
        data = {
            "email": "manager@example.com"
        }
        response = self.stack.unshare(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/unshare")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


if __name__ == '__main__':
    unittest.main()
