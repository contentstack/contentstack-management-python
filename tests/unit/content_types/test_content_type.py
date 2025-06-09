import unittest


import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
content_type_uid = credentials["content_type_uid"]



class ContentTypeUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_content_types(self):
        response = self.client.stack(api_key).content_types().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types?include_count=false&include_global_field_schema=true&include_branch=false")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)
        
    def test_get_all_content_types_with_params(self):
        query = self.client.stack(api_key).content_types()
        query.add_param("include_count", True)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types?include_count=True&include_global_field_schema=true&include_branch=false")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_content_types(self):
        response = self.client.stack(api_key).content_types(content_type_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}?include_global_field_schema=true&include_branch=false")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)
        
    def test_get_a_content_types_with_params(self):
        query = self.client.stack(api_key).content_types(content_type_uid)
        query.add_param("include_branch", True)
        response = query.fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}?include_global_field_schema=true&include_branch=True")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create(self):
        data = {
            "content_type": {
                "title": "test content type",
                "uid": "content_type_uid",
                "schema": [{
                    "display_name": "Title",
                    "uid": "title",
                    "data_type": "text",
                    "field_metadata": {
                        "_default": True
                    },
                    "unique": False,
                    "mandatory": True,
                    "multiple": False
                },
                    {
                        "display_name": "URL",
                        "uid": "url",
                        "data_type": "text",
                        "field_metadata": {
                            "_default": True
                        },
                        "unique": False,
                        "multiple": False
                    }
                ],
                "options": {
                    "title": "title",
                    "publishable": True,
                    "is_page": True,
                    "singleton": False,
                    "sub_title": [
                        "url"
                    ],
                    "url_pattern": "/:title",
                    "url_prefix": "/"
                }
            }
        }
        response = self.client.stack(api_key).content_types().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_content_types(self):
        data = {
            "content_type": {
                "title": "updated content type",
                "uid": "updated_content_type",
                "schema": [{
                    "display_name": "Title",
                    "uid": "title",
                    "data_type": "text",
                    "field_metadata": {
                        "_default": True
                    },
                    "unique": False,
                    "mandatory": True,
                    "multiple": False
                },
                    {
                        "display_name": "URL",
                        "uid": "url",
                        "data_type": "text",
                        "field_metadata": {
                            "_default": True
                        },
                        "unique": False,
                        "multiple": False
                    }
                ],
                "options": {
                    "title": "title",
                    "publishable": True,
                    "is_page": True,
                    "singleton": False,
                    "sub_title": [
                        "url"
                    ],
                    "url_pattern": "/:title",
                    "url_prefix": "/"
                }
            }
        }
        response = self.client.stack(api_key).content_types(content_type_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_set_field_visibility_rule(self):
        data = {
            "content_type": {
                "title": "updatedContentType",
                "uid": "content_type_uid",
                "schema": [{
                    "display_name": "Title",
                    "uid": "title",
                    "data_type": "text",
                    "field_metadata": {
                        "_default": True
                    },
                    "unique": False,
                    "mandatory": True,
                    "multiple": False
                },
                    {
                        "display_name": "URL",
                        "uid": "url",
                        "data_type": "text",
                        "field_metadata": {
                            "_default": True
                        },
                        "unique": False,
                        "multiple": False
                    },
                    {
                        "display_name": "Single Line Textbox",
                        "uid": "single_line_textbox",
                        "data_type": "text",
                        "field_metadata": {
                            "_default": True
                        },
                        "unique": False,
                        "multiple": False
                    },
                    {
                        "display_name": "Multi Line Textbox",
                        "uid": "multi_line_textbox",
                        "data_type": "text",
                        "field_metadata": {
                            "_default": True
                        },
                        "unique": False,
                        "multiple": False
                    }
                ],
                "field_rules": [{
                    "conditions": [{
                        "operand_field": "single_line_textbox",
                        "operator": "equals",
                        "value": "abc"
                    }],
                    "match_type": "all",
                    "actions": [{
                        "action": "show",
                        "target_field": "multi_line_textbox"
                    }]
                }],
                "options": {
                    "title": "title",
                    "publishable": True,
                    "is_page": True,
                    "singleton": False,
                    "sub_title": ["url"],
                    "url_pattern": "/:title",
                    "url_prefix": "/"
                }
            }
        }
        response = self.client.stack(api_key).content_types(
            content_type_uid).set_field_visibility_rules(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_content_types(self):
        response = self.client.stack(api_key).content_types(content_type_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}?force=true")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_get_all_references(self):
        response = self.client.stack(api_key).content_types(content_type_uid).references()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}/references?include_global_fields"
                         f"=true&include_branch=false")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_export(self):
        response = self.client.stack(api_key).content_types(content_type_uid).export()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}/export")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_imports(self):
        file_path = "tests/resources/mock_content_type/import.json"
        response = self.client.stack(api_key).content_types().imports(file_path)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/import")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "multipart/form-data")


if __name__ == '__main__':
    unittest.main()
