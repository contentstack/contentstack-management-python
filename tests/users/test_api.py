import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class UserApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

    def test_get_user(self):    
        response = self.client.user().get() 
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        url = "user"
        user_data = {
                    "user": {
                        "company": "company name inc.",
                        "first_name": "sunil B Lak"
                    }
                }
        act_data = json.dumps(user_data)
        response = self.client.user().update_user(act_data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Profile updated successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

            
       

    def test_active_user(self):
        url = f"user/activate/{os.getenv('user_activation_token')}"
        act_data = {
            "user": {
            "first_name": "your_first_name",
            "last_name": "your_last_name",
            "password": "your_password",
            "password_confirmation": "confirm_your_password"
            }
            }
        act_data = json.dumps(act_data)
        response = self.client.user().active_user(os.getenv('user_activation_token'), act_data) 
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your account has been activated.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)


    def test_request_password(self):
        url = f"user/forgot_password"
        act_data ={
                    "user": {
                        "email": os.getenv("email")
                    }
                }
        act_data = json.dumps(act_data)
        response = self.client.user().request_password(act_data) 
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("If this email address exists, we will send you an email with instructions for resetting your password.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 400)

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
        result_json = response.json()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Your password has been reset successfully.", result_json.get('notice'))
        elif response.status_code == 422:
            self.assertEqual(response.status_code, 422)
            self.assertTrue(result_json.get('error_message'))
            self.assertEqual("The token provided is invalid. Please try again.", result_json['errors']['reset_password_token'][0])

        else:
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
