import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
locale_code = credentials["locale_code"]

class LocaleApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_locale(self):
        response = self.client.stack(api_key).locale().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}locales")
        self.assertEqual(response.status_code, 200)

    def test_get_a_locale(self):
        response = self.client.stack(api_key).locale(locale_code).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}locales/{locale_code}")
        self.assertEqual(response.status_code, 200)


    def test_create(self):
        data = {
                "locale":{
                    "name":"Telugu",
                    "code":"TE",
                    "fallback_locale":"en-us"
                }
                }
        response = self.client.stack(api_key).locale().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}locales")
        self.assertEqual(response.status_code, 201)

    def test_update_locale(self):
        data = {
                "locale":{
                    "name":"Updated Locale Name",
                    "fallback_locale":"en-us"
                }
                }
        response = self.client.stack(api_key).locale(locale_code).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}locales/{locale_code}")
        self.assertEqual(response.status_code, 200)


    def test_delete_locale(self):
        response = self.client.stack(api_key).locale(locale_code).delete()
        self.assertEqual(response.status_code, 200)

    def test_set_fallback(self):
        data = {
                "locale": {
                    "name": "German - German",
                    "code": "de-de",
                    "fallback_locale": "de-en"
                }
                }
        response = self.client.stack(api_key).locale().set_fallback(data)
        self.assertEqual(response.status_code, 200)

    def test_update_fallback(self):
        data = {
                "locale": {
                    "name": "German",
                    "code": "de",
                    "fallback_locale": "en-us"
                    }
                }
        response = self.client.stack(api_key).locale(locale_code).update_fallback(data)
        self.assertEqual(response.status_code, 200)

    