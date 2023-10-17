import os
import unittest

from dotenv import load_dotenv

import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
log_item_uid = credentials["log_item_uid"]


class auditlogesApiTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_auditloges(self):
        response = self.client.stack(api_key).auditlog().find()
        self.assertEqual(response.status_code, 200)

    def test_get_a_auditlog(self):
        response = self.client.stack(api_key).auditlog(log_item_uid).fetch()
        self.assertEqual(response.status_code, 200)

    def test_get_all_auditloges_with_params(self):
        query = self.client.stack(api_key).auditlog()
        query.add_param("include_branch", True)
        response = query.find()
        self.assertEqual(response.status_code, 200)

    def test_get_a_auditlog_with_params(self):
        query = self.client.stack(api_key).auditlog(log_item_uid)
        query.add_param("include_branch", True)
        response = query.fetch()
        self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        unittest.main()