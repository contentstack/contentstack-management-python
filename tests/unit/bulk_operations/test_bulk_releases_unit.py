import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]

class BulkOperationReleaseUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_add_items(self):
        data = {
            "release": "release_uid",
            "action": "publish",
            "locale": ["en-us", "hi-in"],
            "reference": True,
            "items": [
                {
                "uid": "blt63177c0f00f20b61",
                "content_type_uid": "my_blog"
                }
            ]
            }

        response = self.client.stack('api_key').bulk_operation().add_items(data,headers={"bulk_version":"2.0"})
        self.assertEqual(response.request.url, f"{self.client.endpoint}bulk/release/items")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_items(self):
        data = {
                "release": "release_uid",
                "items": [
                    {
                        "uid": "entry_uid",
                        "locale": "en-us"
                    },
                    {
                        "uid": "entry_uid",
                        "locale": "en-us",
                        "variant_id": "entry_variant_id"
                    }
                ]
                or
                [ '$all' ]
            }

        response = self.client.stack('api_key').bulk_operation().update_items(data, headers={"bulk_version":"2.0"})
        self.assertEqual(response.request.url, f"{self.client.endpoint}bulk/release/update_items")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_job_status(self):
        response = self.client.stack('api_key').bulk_operation().job_status('job_uid', headers={"bulk_version":"2.0"})
        self.assertEqual(response.request.url, f"{self.client.endpoint}bulk/jobs/job_uid")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")