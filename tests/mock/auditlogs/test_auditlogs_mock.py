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
log_item_uid = credentials["log_item_uid"]


class AuditlogMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)
 
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_auditlogs/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_all_auditlogs(self):    
        response = self.client.stack(api_key).auditlog().find().json()
        read_mock_auditlogs_data  = self.read_file("find.json")
        mock_auditlogs_data = json.loads(read_mock_auditlogs_data)
        self.assertEqual(mock_auditlogs_data.keys(), response.keys())

    def test_mock_get_a_auditlog(self):    
        response = self.client.stack(api_key).auditlog(log_item_uid).fetch().json()
        read_mock_auditlogs_data  = self.read_file("fetch.json")
        mock_auditlogs_data = json.loads(read_mock_auditlogs_data)
        self.assertEqual(mock_auditlogs_data.keys(), response.keys())

    
if __name__ == '__main__':
    unittest.main()
