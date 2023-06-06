import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class BranchTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)
 
    def read_file(self, file_name):
        file_path= f"tests/resources/mockBranch/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_all_branches(self):    
        response = self.client.stack(os.getenv("API_KEY")).branch().find().json()
        read_mock_branch_data = self.read_file("findAllBranches.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual(mock_branch_data.keys(), response.keys())

    def test_mock_get_a_branch(self):    
        branch_uid = os.getenv("BRANCH_UID")
        response = self.client.stack(os.getenv("API_KEY")).branch(branch_uid).fetch().json()
        read_mock_branch_data = self.read_file("fetchBranch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        uid = mock_branch_data['branch']['uid']
        self.assertEqual("release", uid)

    def test_mock_create_branch(self):    
        data = {
        "branch": {
            "uid": "release",
            "source": "main"
            }
        }
        response = self.client.stack(os.getenv("API_KEY")).branch().create(data).json()
        read_mock_branch_data = self.read_file("createBranch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual("Your request to create branch is in progress. Please check organization bulk task queue for more details.", mock_branch_data['notice'])

    def test_mock_delete_branch(self):    
        response = self.client.stack(os.getenv("API_KEY")).branch().delete().json()
        read_mock_branch_data = self.read_file("deleteBranch.json")
        mock_branch_data = json.loads(read_mock_branch_data)
        self.assertEqual("Your request to delete branch is in progress. Please check organization bulk task queue for more details.", mock_branch_data['notice'])

if __name__ == '__main__':
    unittest.main()
