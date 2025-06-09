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

class TermsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)


    def test_get_a_terms(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

        
    def test_create(self):
        data = {
                "term": {
                    "uid": "term_1",
                    "name": "Term 1",
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_update(self):
        data = {
                "term": {
                    "name": "Term 1"
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_search(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms().search(terms_string)
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms?term={terms_string}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.body, None)

    def test_move(self):
        data = {
                "term": {
                    "parent_uid": None
                }
                }
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).move(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_ancestors(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).ancestors()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}/ancestors")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    
    def test_descendants(self):
        response = self.client.stack(api_key).taxonomy(taxonomy_uid).terms(terms_uid).descendants()
        self.assertEqual(response.request.url, f"{self.client.endpoint}taxonomies/{taxonomy_uid}/terms/{terms_uid}/descendants")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

if __name__ == '__main__':
    unittest.main()
