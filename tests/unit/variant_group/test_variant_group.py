import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
variant_group_uid = credentials["variant_group_uid"]

class VariantGroupUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_find_all_variant_groups(self):
        response = self.client.stack(api_key).variant_group().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_variant_groups_with_params(self):
        query = self.client.stack(api_key).variant_group()
        query.add_param("limit", 10)
        query.add_param("skip", 0)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups?limit=10&skip=0")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_query_variant_groups(self):
        query_params = {"name": "Colors"}
        response = self.client.stack(api_key).variant_group().query(query_params).find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups?name=Colors")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_variant_group(self):
        response = self.client.stack(api_key).variant_group(variant_group_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_variant_group_with_params(self):
        query = self.client.stack(api_key).variant_group(variant_group_uid)
        query.add_param("include_count", True)
        response = query.fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}?include_count=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_variant_group(self):
        data = {
            "variant_group": {
                "name": "Colors",
                "content_types": [
                    "iphone_product_page"
                ],
                "description": "Color variants for product pages"
            }
        }
        response = self.client.stack(api_key).variant_group().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_variant_group(self):
        data = {
            "variant_group": {
                "name": "Updated Colors",
                "content_types": [
                    "iphone_product_page",
                    "android_product_page"
                ],
                "description": "Updated color variants for product pages"
            }
        }
        response = self.client.stack(api_key).variant_group(variant_group_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_variant_group(self):
        response = self.client.stack(api_key).variant_group(variant_group_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_validate_uid_with_valid_uid(self):
        variant_group = self.client.stack(api_key).variant_group(variant_group_uid)
        # This should not raise an exception
        try:
            variant_group.validate_uid()
        except Exception as e:
            self.fail(f"validate_uid() raised {type(e).__name__} unexpectedly!")

    def test_validate_uid_with_invalid_uid(self):
        variant_group = self.client.stack(api_key).variant_group("")
        with self.assertRaises(Exception):
            variant_group.validate_uid()

    def test_validate_uid_with_none_uid(self):
        variant_group = self.client.stack(api_key).variant_group(None)
        with self.assertRaises(Exception):
            variant_group.validate_uid()

if __name__ == '__main__':
    unittest.main()
