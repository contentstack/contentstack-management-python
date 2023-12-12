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
branch_uid = credentials["branch_uid"]


class BranchMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack_management.Client(host = host)
        self.client.login(username, password)
 
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_branch/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_all_branches(self):    
        response = self.client.stack(api_key).branch().find().json()
        read_mock_branch_data = self.read_file("find_all_branches.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual(mock_branch_data.keys(), response.keys())

    def test_mock_get_a_branch(self):    
        response = self.client.stack(api_key).branch(branch_uid).fetch().json()
        read_mock_branch_data = self.read_file("fetch_branch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        uid = mock_branch_data['branch']['uid']
        self.assertEqual("test_get", uid)

    def test_mock_create_branch(self):    
        data = {
        "branch": {
            "uid": "release",
            "source": "main"
            }
        }
        response = self.client.stack(api_key).branch().create(data).json()
        read_mock_branch_data = self.read_file("create_branch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual("Your request to create branch is in progress. Please check organization bulk task queue for more details.", mock_branch_data['notice'])

    def test_mock_delete_branch(self):    
        response = self.client.stack(api_key).branch().delete().json()
        read_mock_branch_data = self.read_file("delete_branch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual("Your request to delete branch is in progress. Please check organization bulk task queue for more details.", mock_branch_data['notice'])

if __name__ == '__main__':
    unittest.main()
