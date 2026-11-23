import json
import unittest
from unittest import mock


import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
branch_uid = credentials["branch_uid"]


class BranchesUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_branches(self):
        response = self.client.stack(api_key).branch().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_branch(self):
        data = {
            "branch": {
                "uid": "release",
                "source": "main"
            }
        }
        response = self.client.stack(api_key).branch().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_branch(self):
        response = self.client.stack(api_key).branch(branch_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}stacks/branches/{branch_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


class BranchCreateEnvironmentsUnitTests(unittest.TestCase):
    """Branch create with publish_config.environments, mocked at the HTTP layer (no credentials)."""

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.requests_patch = mock.patch("contentstack_management._api_client.requests.request")
        self.request = self.requests_patch.start()
        self.request.return_value = mock.Mock(status_code=200, json=lambda: {"branch": {"uid": "release"}})
        self.addCleanup(self.requests_patch.stop)

    def _create(self, data):
        return self.client.stack(api_key).branch().create(data)

    def _posted_body(self):
        self.assertEqual(self.request.call_count, 1)
        kwargs = self.request.call_args.kwargs
        self.assertEqual(self.request.call_args.args[0], "POST")
        self.assertEqual(self.request.call_args.args[1], f"{self.client.endpoint}stacks/branches")
        return json.loads(kwargs["data"])

    def test_two_environment_names_are_posted_as_given(self):
        data = {"branch": {"uid": "release", "source": "main",
                           "publish_config": {"environments": ["development", "staging"]}}}
        self._create(data)
        self.assertEqual(self._posted_body(), data)

    def test_empty_environment_list_is_posted_as_empty_list(self):
        data = {"branch": {"uid": "release", "source": "main", "publish_config": {"environments": []}}}
        self._create(data)
        self.assertEqual(self._posted_body()["branch"]["publish_config"], {"environments": []})

    def test_duplicates_long_list_and_mixed_case_are_posted_unchanged(self):
        cases = [
            ["development", "development"],
            [f"env_{i}" for i in range(150)],
            ["Development", " staging ", "PRODUCTION"],
        ]
        for environments in cases:
            with self.subTest(count=len(environments)):
                self.request.reset_mock()
                self._create({"branch": {"uid": "release", "source": "main",
                                         "publish_config": {"environments": environments}}})
                self.assertEqual(self._posted_body()["branch"]["publish_config"]["environments"], environments)

    def test_omitted_environment_list_posts_todays_body(self):
        data = {"branch": {"uid": "release", "source": "main"}}
        self._create(data)
        self.assertEqual(self._posted_body(), data)
        self.assertNotIn("publish_config", self._posted_body()["branch"])

    def test_empty_publish_config_is_posted_as_empty_object(self):
        self._create({"branch": {"uid": "release", "source": "main", "publish_config": {}}})
        self.assertEqual(self._posted_body()["branch"]["publish_config"], {})

    def test_api_422_for_environment_list_is_returned_unchanged(self):
        api_body = {
            "error_message": "Environment not found.",
            "error_code": 422,
            "errors": {"publish_config.environments": ["no_such_env"]},
        }
        self.request.return_value = mock.Mock(status_code=422, json=lambda: api_body)
        response = self._create({"branch": {"uid": "release", "source": "main",
                                            "publish_config": {"environments": ["development", "no_such_env"]}}})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), api_body)
        self.assertEqual(self._posted_body()["branch"]["publish_config"]["environments"],
                         ["development", "no_such_env"])
