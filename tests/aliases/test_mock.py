import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class AliasMockTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)
 
    def read_file(self, file_name):
        file_path= f"tests/resources/mockAlias/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_all_aliases(self):    
        response = self.client.stack(os.getenv("API_KEY")).branchAlias().fetchAll().json()
        read_mock_alias_data = self.read_file("fetch_all_aliases.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual(mock_alias_data.keys(), response.keys())

    def test_mock_get_a_alias(self):    
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).fetch().json()
        read_mock_alias_data = self.read_file("fetch_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        alias_uid = mock_alias_data['branch_alias']['alias']
        self.assertEqual("alias_uid", alias_uid)

    def test_mock_create_or_update_alias(self):
        data = {
            "branch_alias": {
                "target_branch": "test"
                }
            }
        branch_test_uid = os.getenv("BRANCH_TEST_UID")
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).assign(branch_test_uid, data).json()
        read_mock_alias_data = self.read_file("assign_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual("Branch alias assigned successfully.", mock_alias_data['notice'])


    def test_mock_delete_alias(self):
        branch_alias_uid = os.getenv("BRANCH_ALIAS_UID")
        response = self.client.stack(os.getenv("API_KEY")).branchAlias(branch_alias_uid).delete().json()
        read_mock_alias_data = self.read_file("delete_alias.json")
        mock_alias_data = json.loads(read_mock_alias_data)
        self.assertEqual("Branch alias deleted successfully.", mock_alias_data['notice'])

if __name__ == '__main__':
    unittest.main()
