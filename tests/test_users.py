import unittest
from config2.config import config
from contentstack_management import contentstack

from contentstack_management import contentstack

class UserTests(unittest.TestCase):

    def setUp(self):
        config.get_env()
        config.get()
        self.client = contentstack.client(host=config.host.host)
        self.client.login(config.login.email, config.login.password)

    def test_get_user(self):    
        response = self.client.user().get() 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/user")
        self.assertEqual(response.request.method, "GET")

    def test_active_user(self):
        url = f"user/activate/{config.user.user_activation_token}"
        act_data = {
            "user": {
            "first_name": "your_first_name",
            "last_name": "your_last_name",
            "password": "your_password",
            "password_confirmation": "confirm_your_password"
            }
            }
        response = self.client.user().active_user(config.user.user_activation_token, act_data) 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling

    def test_request_password(self):
        url = f"user/forgot_password"
        act_data ={
                    "user": {
                        "email": "your_email_id"
                    }
                }
        response = self.client.user().request_password(act_data) 
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/{url}")
        self.assertEqual(response.request.method, "POST")
        # Additional assertions for error handling



if __name__ == '__main__':
    unittest.main()
