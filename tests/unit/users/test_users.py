import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
activation_token = credentials["activation_token"]


class UserUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_user(self):
        response = self.client.user().fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}user")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_update_user(self):
        url = "user"
        user_data = {
            "user": {
                "company": "company name inc.",
                "first_name": "Sunil",
                "last_name": "Lakshman",
            }
        }
        response = self.client.user().update(user_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}{url}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_active_user(self):
        url = f"user/activate/{activation_token}"
        act_data = {
            "user": {
                "first_name": "your_first_name",
                "last_name": "your_last_name",
                "password": "your_password",
                "password_confirmation": "confirm_your_password"
            }
        }
        response = self.client.user().activate(activation_token, act_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}{url}")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_request_password(self):
        url = "user/forgot_password"
        act_data = {
            "user": {
                "email": username
            }
        }
        response = self.client.user().forgot_password(act_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}{url}")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_reset_password(self):
        url = "user/reset_password"
        act_data = {
            "user": {
                "reset_password_token": "****",
                "password": "Simple@123",
                "password_confirmation": "Simple@123"
            }
        }
        response = self.client.user().reset_password(act_data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}{url}")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


if __name__ == '__main__':
    unittest.main()
