import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
publish_queue_uid = credentials["publish_queue_uid"]


class publish_queueMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_publish_queue/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_publish_queue(self):
        response = self.client.stack(api_key).publish_queue().find().json()
        read_mock_publish_queue_data  = self.read_file("find.json")
        mock_publish_queue_data = json.loads(read_mock_publish_queue_data)
        self.assertEqual(mock_publish_queue_data.keys(), response.keys())

    def test_get_a_publish_queue(self):
        response = self.client.stack(api_key).publish_queue(publish_queue_uid).fetch().json()
        read_mock_publish_queue_data  = self.read_file("fetch.json")
        mock_publish_queue_data = json.loads(read_mock_publish_queue_data)
        self.assertEqual(mock_publish_queue_data.keys(), response.keys())

    def test_cancel_a_publish_queue(self):
        response = self.client.stack(api_key).publish_queue(publish_queue_uid).cancel().json()
        read_mock_publish_queue_data  = self.read_file("cancel.json")
        mock_publish_queue_data = json.loads(read_mock_publish_queue_data)
        self.assertEqual(mock_publish_queue_data.keys(), response.keys())

    