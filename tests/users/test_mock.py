import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class UserTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

    def read_file(self, file_name):
        file_path= f"tests/resources/mockuser/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data

    def test_mock_get_user(self):    
        response = self.client.user().get().json()
        read_mock_user_data = self.read_file("getuser.json")
        mock_user_data = json.loads(read_mock_user_data)
        authtoken = self.client.get_authtoken(mock_user_data)
        self.assertEqual("the_fake_uid", authtoken)
        self.assertEqual(mock_user_data.keys(), response.keys())

    def test_mock_active_user(self):
        url = f"user/activate/{os.getenv('user_activation_token')}"
        act_data = {
            "user": {
            "first_name": "your_first_name",
            "last_name": "your_last_name",
            "password": "your_password",
            "password_confirmation": "confirm_your_password"
            }
            }

        response = self.client.user().active_user(os.getenv('user_activation_token'), act_data).json()
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
        act_data = json.dumps(user_data)
        response = self.client.user().update_user(act_data).json()
        read_mock_user_data = self.read_file("updateuser.json")
        mock_user_data = json.loads(read_mock_user_data)
        uid = mock_user_data['user']['uid']
        self.assertEqual("its_just_a_fake_uid", uid)
        self.assertEqual(mock_user_data['notice'], response['notice'])


    def test_request_password(self):
        url = f"user/forgot_password"
        act_data ={
                    "user": {
                        "email": "john.doe@contentstack.com"
                    }
                }
        act_data = json.dumps(act_data)
        response = self.client.user().request_password(act_data).json()
        read_mock_user_data = self.read_file("request_password.json")
        mock_user_data = json.loads(read_mock_user_data)
        self.assertEqual(mock_user_data['notice'], response['notice'])

    def test_reset_password(self):
        url = f"user/reset_password"
        act_data = {
                    "user": {
                        "reset_password_token": "abcdefghijklmnop1234567890",
                        "password": "Simple@123",
                        "password_confirmation": "Simple@123"
                    }
                }
        act_data = json.dumps(act_data)
        response = self.client.user().reset_password(act_data) 
        read_mock_user_data = self.read_file("reset_password.json")
        mock_user_data = json.loads(read_mock_user_data)
        self.assertEqual("Your password has been reset successfully.", mock_user_data['notice'])



if __name__ == '__main__':
    unittest.main()
