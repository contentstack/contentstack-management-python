import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
activation_token = credentials["activation_token"]


class UserApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_user(self):
        response = self.client.user().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 401)

    def test_update_user(self):
        user_data = {
            "user": {
                "company": "company name inc.",
                "first_name": "sunil B Lak"
            }
        }
        response = self.client.user().update(user_data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Profile updated successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 401)

    def test_active_user(self):
        act_data = {
            "user": {
                "first_name": "your_first_name",
                "last_name": "your_last_name",
                "password": "your_password",
                "password_confirmation": "confirm_your_password"
            }
        }
        response = self.client.user().activate(activation_token, act_data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your account has been activated.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_forgot_password(self):
        act_data = {
            "user": {
                "email": username
            }
        }
        response = self.client.user().forgot_password(act_data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual(
                "If this email address exists, we will send you an email with instructions for resetting your password.",
                result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

    def test_reset_password(self):
        act_data = {
            "user": {
                "reset_password_token": "abcdefghijklmnop1234567890",
                "password": "Simple@123",
                "password_confirmation": "Simple@123"
            }
        }
        response = self.client.user().reset_password(act_data)
        result_json = response.json()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your password has been reset successfully.", result_json.get('notice'))
        elif response.status_code == 422:
            self.assertEqual(response.status_code, 422)
            self.assertTrue(result_json.get('error_message'))
            self.assertEqual("The token provided is invalid. Please try again.",
                             result_json['errors']['reset_password_token'][0])

        else:
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
