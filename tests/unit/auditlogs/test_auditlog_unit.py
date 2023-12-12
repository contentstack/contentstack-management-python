import os
import unittest

from dotenv import load_dotenv

import contentstack_management
from contentstack_management._errors import ArgumentException
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
log_item_uid = credentials["log_item_uid"]


class auditlogesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_auditloges(self):
        response = self.client.stack(api_key).auditlog().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}audit-logs")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_auditlog(self):
        response = self.client.stack(api_key).auditlog(log_item_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}audit-logs/{log_item_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_auditlog_invalid_input(self):
        try: 
            response = self.client.stack(api_key).auditlog().fetch()
        except ArgumentException as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "Log item Uid is required", e.args[0])

    def test_get_all_auditloges_with_params(self):
        query = self.client.stack(api_key).auditlog()
        query.add_param("include_branch", True)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}audit-logs?include_branch=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_auditlog_with_params(self):
        query = self.client.stack(api_key).auditlog(log_item_uid)
        query.add_param("include_branch", False)
        response = query.fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}audit-logs/{log_item_uid}?include_branch=False")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    # if __name__ == '__main__':
    #     unittest.main()