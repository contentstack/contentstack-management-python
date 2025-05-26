import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
webhooks_uid = credentials["webhook_uid"]
webhook_execution_uid = credentials["webhook_execution_uid"]

class ContentTypeMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_webhooks/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_webhooks(self):
        response = self.client.stack(api_key).webhooks().find().json()
        read_mock_webhooks_data  = self.read_file("find.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data.keys(), response.keys())

    def test_get_a_webhooks(self):
        response = self.client.stack(api_key).webhooks(webhooks_uid).fetch().json()
        read_mock_webhooks_data  = self.read_file("fetch.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data.keys(), response.keys())

    def test_create(self):
        data ={
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
        response = self.client.stack(api_key).webhooks().create(data).json()
        read_mock_webhooks_data  = self.read_file("create.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data['notice'], response["notice"])

    def test_update_webhooks(self):
        data = {
                "webhook":{
                    "name":"Updated webhook",
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
                    "channels":[
                    "assets.create"
                    ],
                    "branches":[
                    "main"
                    ],
                    "retry_policy":"manual",
                    "disabled":True,
                    "concise_payload":False
                }
                }
        response = self.client.stack(api_key).webhooks(webhooks_uid).update(data).json()
        read_mock_webhooks_data  = self.read_file("update.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual( mock_webhooks_data['notice'], response['notice'])

    def test_delete_webhooks(self):
        response = self.client.stack(api_key).webhooks(webhooks_uid).delete().json()
        read_mock_webhooks_data  = self.read_file("delete.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual("The Webhook was deleted successfully", mock_webhooks_data['notice'])
        
    def test_get_all_executions(self):
        query = self.client.stack(api_key).webhooks(webhooks_uid)
        query1 = query.add_param("from", "2023-07-01T12:34:36.000Z")
        query2 = query.add_param("to", "2016-07-31T12:34:36.000Z")
        response = query.executions().json()
        read_mock_webhooks_data  = self.read_file("executions.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data.keys(), response.keys())

    def test_export(self):
        response = self.client.stack(api_key).webhooks(webhooks_uid).export().json()
        read_mock_webhooks_data  = self.read_file("export.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data.keys(), response.keys())

    def test_imports(self):
        file_path = "tests/resources/mock_webhooks/import.json"
        response = self.client.stack(api_key).webhooks().imports(file_path).json
        read_mock_webhooks_data  = self.read_file("import.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual("The Webhook was imported successfully", mock_webhooks_data['notice'])

    def test_logs(self):
        response = self.client.stack(api_key).webhooks().logs(webhook_execution_uid).json()
        read_mock_webhooks_data  = self.read_file("logs.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual(mock_webhooks_data.keys(), response.keys())

    def test_retry_webhooks(self):
        response = self.client.stack(api_key).webhooks().retry(webhook_execution_uid).json()
        read_mock_webhooks_data  = self.read_file("retry.json")
        mock_webhooks_data = json.loads(read_mock_webhooks_data)
        self.assertEqual("Webhook retry scheduled" ,mock_webhooks_data['notice'])


if __name__ == '__main__':
    unittest.main()
