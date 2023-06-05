import unittest
import os
from dotenv import load_dotenv


from contentstack_management import contentstack


# from contentstack import management

def load_api_keys():
    load_dotenv()

class ContentstackTests(unittest.TestCase):
    
    def setUp(self):
        load_api_keys()
        self.client = contentstack.client(host=os.getenv("host"))
        self.client.login(os.getenv("email"), os.getenv("password"))

    def test_contentstack(self):
        client = contentstack.client(host=os.getenv("host"), endpoint=None)
        self.assertEqual('api.contentstack.io', client.host)  # add assertion here

    
    def test_successful_get_login(self):
        client = contentstack.client(host=os.getenv("host"))
        response = client.login(os.getenv("email"), os.getenv("password"))
        self.assertEqual(response.status_code, 200)

    def test_error_email_id(self):
        try:
            self.client = contentstack.client(host=os.getenv("host"))
            self.client.login('', os.getenv("password"))
            self.assertEqual(None, self.client.email)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid email id'", e.args[0])
                
    def test_error_password(self):
        try:
            self.client = contentstack.client(host=os.getenv("host"))
            self.client.login(os.getenv("email"),'')
            self.assertEqual(None, self.client.password)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid password'", e.args[0])



if __name__ == '__main__':
    unittest.main()
