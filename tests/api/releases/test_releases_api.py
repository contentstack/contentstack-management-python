import os
import unittest
from dotenv import load_dotenv
<<<<<<< HEAD
from contentstack_management import contentstack
=======
import contentstack_management
>>>>>>> fff0f0fb49c9346070ad6dbf76e64808c5aeb364
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
release_uid = credentials["release_uid"]



class ReleaseApiTests(unittest.TestCase):

    def setUp(self):
<<<<<<< HEAD
        self.client = contentstack.ContentstackClient(host=host)
=======
        self.client = contentstack_management.Client(host=host)
>>>>>>> fff0f0fb49c9346070ad6dbf76e64808c5aeb364
        self.client.login(username, password)

    def test_get_all_releases(self):
        response = self.client.stack(api_key).releases().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases")
        self.assertEqual(response.status_code, 200)

    def test_get_a_releases(self):
        response = self.client.stack(api_key).releases(release_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}releases/{release_uid}")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
                "release": {
                    "name": "Release name",
                    "description": "2023-09-27",
                    "locked": False,
                    "archived": False
                }
            }
        response = self.client.stack(api_key).releases().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases")
        self.assertEqual(response.status_code, 201)

    def test_update_releases(self):
        data = {
                "release": {
                    "name": "Release Name",
                    "description": "2018-12-22"
                }
            }
        response = self.client.stack(api_key).releases(release_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}releases/{release_uid}")
        self.assertEqual(response.status_code, 200)


    def test_delete_releases(self):
        response = self.client.stack(api_key).releases(release_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}releases/{release_uid}")
        self.assertEqual(response.status_code, 200)

    
    def test_clone(self):
        data = {
                "release": {
                    "name": "New Release Name",
                    "description": "2018-12-12"
                }
            }
        response = self.client.stack(api_key).releases(release_uid).clone(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}releases/{release_uid}/clone")
        self.assertEqual(response.status_code, 201)

    def test_deploy(self):
        data = {
                "release": {
<<<<<<< HEAD
                    "scheduled_at": "2023-09-27T13:13:13:122Z",
                    "action": "publish",
                    "environments": [
                        "development"
                    ],
                    "locales": [
                        "en-us"
=======
                    "environments": [
                        "development"
>>>>>>> fff0f0fb49c9346070ad6dbf76e64808c5aeb364
                    ]
                }
            }
        response = self.client.stack(api_key).releases(release_uid).deploy(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}releases/{release_uid}/deploy")
        self.assertEqual(response.status_code, 200)

   


if __name__ == '__main__':
    unittest.main()
