import unittest
import json
import os
from dotenv import load_dotenv
from contentstack_management import contentstack

def load_api_keys():
    load_dotenv()

class UserUnitTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

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
        url = f"user/activate/{os.getenv('user_activation_token')}"
        act_data = {
            "user": {
            "first_name": "your_first_name",
            "last_name": "your_last_name",
            "password": "your_password",
            "password_confirmation": "confirm_your_password"
            }
            }
        response = self.client.user().activate(os.getenv('user_activation_token'), act_data) 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling

    def test_request_password(self):
        url = f"user/forgot_password"
        act_data ={
                    "user": {
                        "email": os.getenv("email")
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
