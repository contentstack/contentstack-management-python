import unittest
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
content_type_uid = credentials["content_type_uid"]
entry_uid = credentials["entry_uid"]
variant_uid = credentials["variant_uid"]

class EntryVariantsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_find_all_entry_variants(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_find_entry_variants_with_params(self):
        params = {"limit": 10, "skip": 0}
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants().find(params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants?limit=10&skip=0")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_query_entry_variants(self):
        query = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants()
        query.add_param("title", "variant title")
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants?title=variant+title")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create_entry_variant(self):
        data = {
            "customized_fields": [
                "title",
                "url"
            ],
            "base_entry_version": 10,
            "entry": {
                "title": "example",
                "url": "/example"
            }
        }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_fetch_entry_variant(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_entry_variant_with_params(self):
        params = {"include_count": True}
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).fetch(params=params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}?include_count=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_update_entry_variant(self):
        data = {
            "customized_fields": [
                "title",
                "url",
                "description"
            ],
            "entry": {
                "title": "updated example",
                "url": "/updated-example",
                "description": "Updated description"
            }
        }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_entry_variant(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_versions_entry_variant(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).versions()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}/versions")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_versions_entry_variant_with_params(self):
        params = {"limit": 10, "skip": 0}
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants(variant_uid).versions(params=params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/variants/{variant_uid}/versions?limit=10&skip=0")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_include_variants(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).includeVariants('true', variant_uid)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?include_variants=true&variant_uid={variant_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_include_variants_with_params(self):
        params = {"limit": 10, "skip": 0}
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).includeVariants('true', variant_uid, params)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?limit=10&skip=0&include_variants=true&variant_uid={variant_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_validate_content_type_uid_with_valid_uid(self):
        entry_variants = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants()
        # This should not raise an exception
        try:
            entry_variants.validate_content_type_uid()
        except Exception as e:
            self.fail(f"validate_content_type_uid() raised {type(e).__name__} unexpectedly!")

    def test_validate_content_type_uid_with_invalid_uid(self):
        entry_variants = self.client.stack(api_key).content_types("").entry(entry_uid).variants()
        with self.assertRaises(Exception):
            entry_variants.validate_content_type_uid()

    def test_validate_content_type_uid_with_none_uid(self):
        # Create entry_variants instance directly to test validation
        entry_variants = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants()
        entry_variants.content_type_uid = None
        with self.assertRaises(Exception):
            entry_variants.validate_content_type_uid()

    def test_validate_entry_uid_with_valid_uid(self):
        entry_variants = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).variants()
        # This should not raise an exception
        try:
            entry_variants.validate_entry_uid()
        except Exception as e:
            self.fail(f"validate_entry_uid() raised {type(e).__name__} unexpectedly!")

    def test_validate_entry_uid_with_invalid_uid(self):
        entry_variants = self.client.stack(api_key).content_types(content_type_uid).entry("").variants()
        with self.assertRaises(Exception):
            entry_variants.validate_entry_uid()

    def test_validate_entry_uid_with_none_uid(self):
        entry_variants = self.client.stack(api_key).content_types(content_type_uid).entry(None).variants()
        with self.assertRaises(Exception):
            entry_variants.validate_entry_uid()

if __name__ == '__main__':
    unittest.main()
