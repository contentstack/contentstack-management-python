import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
variant_group_uid = credentials["variant_group_uid"]
variant_uid = credentials["variant_uid"]

class VariantsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_find_all_variants(self):
        response = self.client.stack(api_key).variants().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_variants_with_params(self):
        params = {"limit": 10, "skip": 0}
        response = self.client.stack(api_key).variants().find(params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants?limit=10&skip=0")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_grouped_variants(self):
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_grouped_variants_with_params(self):
        params = {"limit": 10, "skip": 0}
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants().find(params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants?limit=10&skip=0")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_query_variants(self):
        query_params = {"title": "variant title"}
        response = self.client.stack(api_key).variants().query(query_params).find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants?title=variant+title")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_query_grouped_variants(self):
        query_params = {"title": "variant title"}
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants().query(query_params).find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants?title=variant+title")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_variant(self):
        response = self.client.stack(api_key).variants(variant_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants/{variant_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_variant_with_params(self):
        params = {"include_count": True}
        response = self.client.stack(api_key).variants(variant_uid).fetch(params=params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants/{variant_uid}?include_count=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_grouped_variant(self):
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants(variant_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_grouped_variant_with_params(self):
        params = {"include_count": True}
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants(variant_uid).fetch(params=params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants/{variant_uid}?include_count=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_variant(self):
        data = {
            "variant": {
                "title": "Red Variant",
                "description": "Red color variant for products",
                "is_default": False
            }
        }
        response = self.client.stack(api_key).variants().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_create_grouped_variant(self):
        data = {
            "variant": {
                "title": "Red Variant",
                "description": "Red color variant for products",
                "is_default": False
            }
        }
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_variant(self):
        data = {
            "variant": {
                "title": "Updated Red Variant",
                "description": "Updated red color variant for products",
                "is_default": True
            }
        }
        response = self.client.stack(api_key).variants(variant_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants/{variant_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_grouped_variant(self):
        data = {
            "variant": {
                "title": "Updated Red Variant",
                "description": "Updated red color variant for products",
                "is_default": True
            }
        }
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants(variant_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_variant(self):
        response = self.client.stack(api_key).variants(variant_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variants/{variant_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_grouped_variant(self):
        response = self.client.stack(api_key).variant_group(variant_group_uid).variants(variant_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}variant_groups/{variant_group_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_validate_variant_group_uid_with_valid_uid(self):
        variants = self.client.stack(api_key).variant_group(variant_group_uid).variants()
        # This should not raise an exception
        try:
            variants.validate_variant_group_uid()
        except Exception as e:
            self.fail(f"validate_variant_group_uid() raised {type(e).__name__} unexpectedly!")

    def test_validate_variant_group_uid_with_invalid_uid(self):
        variants = self.client.stack(api_key).variant_group("").variants()
        with self.assertRaises(Exception):
            variants.validate_variant_group_uid()

    def test_validate_variant_group_uid_with_none_uid(self):
        variants = self.client.stack(api_key).variant_group(None).variants()
        with self.assertRaises(Exception):
            variants.validate_variant_group_uid()

if __name__ == '__main__':
    unittest.main()
