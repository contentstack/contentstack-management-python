import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
taxonomy_uid = credentials["taxonomy_uid"]
terms_uid = credentials["terms_uid"]
terms_string = credentials["terms_string"]

class TermsApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().find()
        self.assertEqual(response.status_code, 200)


    def test_get_a_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).fetch()
        self.assertEqual(response.status_code, 200)

        
    def test_create(self):
        data = {
                "term": {
                    "uid": "term_190",
                    "name": "Term 190",
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().create(data)
        self.assertEqual(response.status_code, 201)


    def test_update(self):
        data = {
                "term": {
                    "name": "Term 191"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).update(data)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).delete()
        self.assertEqual(response.status_code, 200)


    def test_search(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().search(terms_string)
        self.assertEqual(response.status_code, 200)

    def test_move(self):
        data = {
                "term": {
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).move(data)
        self.assertEqual(response.status_code, 200)

    def test_ancestors(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).ancestors()
        self.assertEqual(response.status_code, 200)

    
    def test_descendants(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).descendants()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
