import unittest

from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
activation_token = credentials["activation_token"]


class UserUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack.client(host=host)
        self.client.login(username, password)

    def test_get_user(self):
        response = self.client.user().find()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/user")
        self.assertEqual(response.request.method, "GET")

    def test_update_user(self):
        url = "user"
        user_data = {
            "user": {
                "company": "company name inc.",
                "first_name": "sunil B Lakshman"
            }
        }
        response = self.client.user().update(user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "PUT")

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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling

    def test_request_password(self):
        url = f"user/forgot_password"
        act_data = {
            "user": {
                "email": username
            }
        }
        response = self.client.user().forgot_password(act_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling

    def test_reset_password(self):
        url = f"user/reset_password"
        act_data = {
            "user": {
                "reset_password_token": "abcdefghijklmnop1234567890",
                "password": "Simple@123",
                "password_confirmation": "Simple@123"
            }
        }
        response = self.client.user().reset_password(act_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling


if __name__ == '__main__':
    unittest.main()
