import json
import unittest

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
activation_token = credentials["activation_token"]


class UserMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def read_file(self, file_name):
        file_path = f"tests/resources/mockuser/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_user(self):
        response = self.client.user().find().json()
        read_mock_user_data = self.read_file("getuser.json")
        mock_user_data = json.loads(read_mock_user_data)
        authtoken = self.client.get_authtoken(mock_user_data)
        self.assertEqual("the_fake_uid", authtoken)
        self.assertEqual(mock_user_data.keys(), response.keys())

    def test_mock_active_user(self):
        url = f"user/activate/{activation_token}"
        act_data = {
            "user": {
                "first_name": "your_first_name",
                "last_name": "your_last_name",
                "password": "your_password",
                "password_confirmation": "confirm_your_password"
            }
        }

        response = self.client.user().activate(activation_token, act_data).json()
        read_mock_user_data = self.read_file("activateuser.json")
        mock_user_data = json.loads(read_mock_user_data)
        self.assertEqual("Your account has been activated.", mock_user_data['notice'])

    def test_mock_user_update(self):
        user_data = {
            "user": {
                "company": "company name inc.",
                "first_name": "sunil B Lakshman"
            }
        }
        response = self.client.user().update(user_data).json()
        read_mock_user_data = self.read_file("updateuser.json")
        mock_user_data = json.loads(read_mock_user_data)
        uid = mock_user_data['user']['uid']
        self.assertEqual("its_just_a_fake_uid", uid)
        self.assertEqual(mock_user_data['notice'], response['notice'])

    def test_request_password(self):
        url = "user/forgot_password"
        act_data = {
            "user": {
                "email": "john.doe@contentstack.com"
            }
        }
        response = self.client.user().forgot_password(act_data).json()
        read_mock_user_data = self.read_file("request_password.json")
        mock_user_data = json.loads(read_mock_user_data)
        self.assertEqual(mock_user_data['notice'], response['notice'])

    def test_reset_password(self):
        url = "user/reset_password"
        act_data = {
            "user": {
                "reset_password_token": "abcdefghijklmnop1234567890",
                "password": "Simple@123",
                "password_confirmation": "Simple@123"
            }
        }
        response = self.client.user().reset_password(act_data).json()
        read_mock_user_data = self.read_file("reset_password.json")
        mock_user_data = json.loads(read_mock_user_data)
        self.assertEqual("Your password has been reset successfully.", mock_user_data['notice'])


if __name__ == '__main__':
    unittest.main()
