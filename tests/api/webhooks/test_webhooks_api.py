import os
import unittest
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
webhook_execution_uid = credentials["webhook_execution_uid"]
webhook_uid = credentials["webhook_uid"]



class WebhooksApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_webhooks(self):
        response = self.client.stack(api_key).webhooks().find()
        self.assertEqual(response.status_code, 200)

    def test_get_a_webhooks(self):
        response = self.client.stack(api_key).webhooks(webhook_uid).fetch()
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
                "webhook":{
                    "name":"Test",
                    "destinations":[
                    {
                        "target_url":"http://example.com",
                        "http_basic_auth":"basic",
                        "http_basic_password":"test",
                        "custom_header":[
                        {
                            "header_name":"Custom",
                            "value":"testing"
                        }
                        ]
                    }
                    ],
                    "notifiers": "dave.joe@gmail.com",
                    "channels":[
                    "assets.create"
                    ],
                    "branches":[
                    "main"
                    ],
                    "retry_policy":"manual",
                    "disabled":False,
                    "concise_payload":True
                }
                }
        response = self.client.stack(api_key).webhooks().create(data)
        self.assertEqual(response.status_code, 201)

    def test_update_webhooks(self):
        data = {
                "webhook":{
                    "name":"Updated Webhook 2",
                    "destinations":[
                    {
                        "target_url":"http://example.com",
                        "http_basic_auth":"basic",
                        "http_basic_password":"test",
                        "custom_header":[
                        {
                            "header_name":"Custom",
                            "value":"testing"
                        }
                        ]
                    }
                    ],
                    "notifiers": "dave.joe@gmail.com",
                    "channels":[
                    "assets.create"
                    ],
                    "branches":[
                    "main"
                    ],
                    "retry_policy":"manual",
                    "disabled":False,
                    "concise_payload":True
                }
                }
        response = self.client.stack(api_key).webhooks(webhook_uid).update(data)
        self.assertEqual(response.status_code, 200)


    def test_delete_webhooks(self):
        response = self.client.stack(api_key).webhooks(webhook_uid).delete()
        self.assertEqual(response.status_code, 200)

    def test_get_executions(self):
        response = self.client.stack(api_key).webhooks(webhook_uid).executions()
        self.assertEqual(response.status_code, 200)

    def test_export(self):
        response = self.client.stack(api_key).webhooks(webhook_uid).export()
        self.assertEqual(response.status_code, 200)

    def test_imports(self):
        file_path = "tests/resources/mock_webhooks/import.json"
        response = self.client.stack(api_key).webhooks().imports(file_path)
        self.assertEqual(response.status_code, 200)

    def test_logs(self):
        response = self.client.stack(api_key).webhooks().logs(webhook_execution_uid)
        self.assertEqual(response.status_code, 200)

    def test_retry_webhooks(self):
        response = self.client.stack(api_key).webhooks().retry(webhook_execution_uid)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
