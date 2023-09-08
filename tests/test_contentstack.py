import unittest

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]


class ContentstackTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.ContentstackClient(host=host)
        self.client.login(username, password)

    def test_client(self):
        client = contentstack.ContentstackClient()
        self.assertEqual('https://api.contentstack.io/v3/', client.endpoint) # Default host 'api.contentstack.io'

    def test_successful_get_login(self):
        client = contentstack.ContentstackClient(host=host)
        response = client.login(username, password)
        self.assertEqual(response.request.url, f"{self.client.endpoint}user-session")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_error_email_id(self):
        try:
            self.client = contentstack.ContentstackClient(host=host)
            self.client.login('', password)
            self.assertEqual(None, self.client.email)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid email id'", e.args[0])

    def test_error_password(self):
        try:
            self.client = contentstack.ContentstackClient(host=host)
            self.client.login(username, '')
            self.assertEqual(None, self.client.password)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid password'", e.args[0])
                
   


if __name__ == '__main__':
    unittest.main()
