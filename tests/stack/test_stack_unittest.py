import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class StacksUnitTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))
        self.api_key = os.getenv("api_key")

    
    def test_stacks_get(self):    
        response = self.client.stack(self.api_key).fetch() 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "GET")


    def test_stacks_all(self):    
        response = self.client.stack().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "GET")

    def tests_stacks_create(self):
        data = {
                "stack": {
                    "name": "My New Stack by testcases1",
                    "description": "My new test stack",
                    "master_locale": "en-us"
                }
                }
        response= self.client.stack().create(os.getenv("org_uid"), data)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "POST")
    
    def tests_stacks_update(self):
        data = {
                "stack": {
                    "name": "My New Stack by test",
                    "description": "My new test stack",
                    "master_locale": "en-us"
                }
                }
        response= self.client.stack(os.getenv("api_key")).update(data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "PUT")

    def tests_stacks_delete(self):
        response= self.client.stack(os.getenv("api_key")).delete()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks")
        self.assertEqual(response.request.method, "DELETE")


    def tests_stacks_fetch_all_user(self):
        response= self.client.stack(os.getenv("api_key")).users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/users")
        self.assertEqual(response.request.method, "GET")

    def tests_stacks_update_user_role(self):
        data = {
                "users": {
                    "user_uid": ["role_uid1", "role_uid2"]
                }
            }
        response= self.client.stack(os.getenv("api_key")).update_user_role(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/users/roles")
        self.assertEqual(response.request.method, "PUT")

    def tests_stacks_transfer_ownership(self):
        data = {
                "transfer_to": "manager@example.com"
            }
        response= self.client.stack(os.getenv("api_key")).transfer_ownership(data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/transfer_ownership")
        self.assertEqual(response.request.method, "POST")

    def tests_stacks_accept_ownership(self):
        response= self.client.stack(os.getenv("api_key")).accept_ownership(os.getenv("user_id"), os.getenv("ownership_token"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/accept_ownership/?api_key={self.api_key}")
        self.assertEqual(response.request.method, "GET")

    def tests_stacks_get_stack_settings(self):
        response= self.client.stack(os.getenv("api_key")).settings()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/settings")
        self.assertEqual(response.request.method, "GET")

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
        response= self.client.stack(os.getenv("api_key")).create_settings(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/settings")
        self.assertEqual(response.request.method, "POST")

    def tests_stacks_reset_stack_settings(self):
        data = {
                "stack_settings":{}
            }
        response= self.client.stack(os.getenv("api_key")).reset_settings(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/settings/reset")
        self.assertEqual(response.request.method, "POST")

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
        response= self.client.stack(os.getenv("api_key")).share(data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/share")
        self.assertEqual(response.request.method, "POST")

    def tests_stacks_unshare_stack(self):
        data = {
                "email": "manager@example.com"
            }
        response= self.client.stack(os.getenv("api_key")).unshare(data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/stacks/unshare")
        self.assertEqual(response.request.method, "POST")

if __name__ == '__main__':
    unittest.main()
