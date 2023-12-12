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
publish_queue_uid = credentials["publish_queue_uid"]

class publish_queueUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_publish_queue(self):
        response = self.client.stack(api_key).publish_queue().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}publish-queue")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_publish_queue(self):
        response = self.client.stack(api_key).publish_queue(publish_queue_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}publish-queue/{publish_queue_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_cancel_a_publish_queue(self):
        response = self.client.stack(api_key).publish_queue(publish_queue_uid).cancel()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}publish-queue/{publish_queue_uid}/unschedule")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    