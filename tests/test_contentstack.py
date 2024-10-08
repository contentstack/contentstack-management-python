import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]


class ContentstackTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_client(self):
        client = contentstack_management.Client(authtoken='your_authtoken')
        self.assertEqual('https://api.contentstack.io/v3/', client.endpoint) # Default host 'api.contentstack.io'

    def test_gcp_na_region(self):
        client = contentstack_management.Client(authtoken='your_authtoken', region='gcp-na')
        self.assertEqual('https://gcp-na-api.contentstack.com/v3/', client.endpoint)

    def test_successful_get_login(self):
        client = contentstack_management.Client(host=host)
        response = client.login(username, password)
        self.assertEqual(response.request.url, f"{self.client.endpoint}user-session")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_error_email_id(self):
        try:
            self.client = contentstack_management.Client(host=host)
            self.client.login('', password)
            self.assertEqual(None, self.client.email)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid email id'", e.args[0])

    def test_error_password(self):
        try:
            self.client = contentstack_management.Client(host=host)
            self.client.login(username, '')
            self.assertEqual(None, self.client.password)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid password'", e.args[0])
                
    def test_earlyaccess(self):
        client = contentstack_management.Client(host=host, early_access=['ea1','ea2'])
        response = client.login(username, password)
        self.assertEqual(response.request.headers["x-header-ea"], "ea1, ea2")


if __name__ == '__main__':
    unittest.main()
