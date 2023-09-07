import json
import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
branch_alias_uid = credentials["branch_alias_uid"]


class AliasMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)
 
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_alias/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_all_aliases(self):    
        response = self.client.stack(api_key).alias().find().json()
        read_mock_alias_data = self.read_file("fetch_all_aliases.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual(mock_alias_data.keys(), response.keys())

    def test_mock_get_a_alias(self):    
        response = self.client.stack(api_key).alias(branch_alias_uid).fetch().json()
        read_mock_alias_data = self.read_file("fetch_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        alias_uid = mock_alias_data['branch_alias']['alias']
        self.assertEqual("alias_uid", alias_uid)

    def test_assign_alias(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
                }
            }
        response = self.client.stack(api_key).alias(branch_alias_uid).assign(data).json()
        read_mock_alias_data = self.read_file("assign_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual("Branch alias assigned successfully.", mock_alias_data['notice'])


    def test_mock_delete_alias(self):
        response = self.client.stack(api_key).alias(branch_alias_uid).delete().json()
        read_mock_alias_data = self.read_file("delete_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual("Branch alias deleted successfully.", mock_alias_data['notice'])

if __name__ == '__main__':
    unittest.main()
