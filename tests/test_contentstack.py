import unittest
from config2.config import config
from contentstack_management import contentstack
class ContentstackTests(unittest.TestCase):
    
    def setUp(self):
        config.get_env()
        config.get()
        self.client = contentstack.client(host=config.host.host)
        self.client.login(config.login.email, config.login.password)

    def test_contentstack(self):
        client = contentstack.client(host=config.host.host, endpoint=None)
        self.assertEqual('eu-api.contentstack.com', client.host)  # add assertion here

    
    def test_successful_get_login(self):
        client = contentstack.client(host=config.host.host)
        response = client.login(config.login.email, config.login.password )
        self.assertEqual(response.status_code, 200)

    def test_error_email_id(self):
        try:
            self.client = contentstack.client(host=config.host.host)
            self.client.login('', config.login.password)
            self.assertEqual(None, self.client.email)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid email id'", e.args[0])
                
    def test_error_password(self):
        try:
            self.client = contentstack.client(host=config.host.host)
            self.client.login(config.login.email,'')
            self.assertEqual(None, self.client.password)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid password'", e.args[0])



if __name__ == '__main__':
    unittest.main()
