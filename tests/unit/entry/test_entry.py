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

class EntryUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_entries(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_all_entries_with_limit(self):
        query = self.client.stack(api_key).content_types(content_type_uid).entry()
        query.add_param("limit", 2)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries?limit=2")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_all_entries_with_skip(self):
        query = self.client.stack(api_key).content_types(content_type_uid).entry()
        query.add_param("skip", 2)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries?skip=2")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_all_entries_with_limit_and_skip(self):
        query = self.client.stack(api_key).content_types(content_type_uid).entry()
        query.add_param("limit", 2)
        query.add_param("skip", 2)
        response = query.find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries?limit=2&skip=2")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)


    def test_get_a_entry(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).fetch()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

        
    def test_create(self):
        data = {
                    "entry": {
                        "title": "example",
                        "url": "/example"
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries?locale={locale}")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_create_json_rte(self):
        data = {
                    "entry":{
                        "title":"Example One",
                        "url":"/example-one",
                        "json_rte":{
                        "children":[
                            {
                            "children":[
                                {
                                "text":"Hello world! This is paragraph 1."
                                }
                            ],
                            "type":"p",
                            "uid":"test-uid",
                            "attrs":{
                            }
                            },
                            {
                            "children":[
                                {
                                "text":"This is paragraph 2. "
                                },
                                {
                                "text":"It has good content. ",
                                "bold":True
                                },
                                {
                                "text":"Enjoy the good reading!",
                                "bold":True,
                                "italic":True,
                                "align":"right"
                                }
                            ],
                            "type":"p",
                            "uid":"test-uid",
                            "attrs":{
                            }
                            },
                            {
                            "children":[
                                {
                                "text":"This is paragraph 3."
                                }
                            ],
                            "type":"p",
                            "uid":"test-uid",
                            "attrs":{
                            }
                            },
                            {
                            "children":[
                                {
                                "text":"Embedded entry:",
                                "bold":True
                                },
                                {
                                "uid":"test-uid",
                                "type":"reference",
                                "attrs":{
                                    "class-name":"embedded-entry redactor-component inline-entry",
                                    "content-type-uid":"test",
                                    "display-type":"inline",
                                    "entry-uid":"entry-uid",
                                    "locale":"en-us",
                                    "type":"entry",
                                },
                                "children":[
                                    {
                                    "text":""
                                    }
                                ]
                                },
                                {
                                "text":"continued text after embedding an entry."
                                }
                            ],
                            "type":"p",
                            "uid":"test-uid",
                            "attrs":{
                            }
                            },
                            {
                            "children":[
                                {
                                "text":"Embedded asset:",
                                "bold":True
                                },
                                {
                                "uid":"test-uid",
                                "type":"reference",
                                "attrs":{
                                    "asset-link":"https://images.contentstack.io/v3/assets/api-key/asset-uid/tech.jpg",
                                    "asset-name":"tech.jpg",
                                    "asset-type":"image/jpg",
                                    "asset-uid":"test-uid",
                                    "class-name":"embedded-asset",
                                    "content-type-uid":"sys_assets",
                                    "display-type":"display",
                                    "inline":True,
                                    "type":"asset",
                                },
                                "children":[
                                    {
                                    "text":""
                                    }
                                ]
                                },
                                {
                                "text":"continued text after embedding an asset",
                                "bold":True
                                }
                            ],
                            "type":"p",
                            "uid":"test-uid",
                            "attrs":{
                            }
                            }
                        ],
                        "type":"doc",
                        "uid":"test-uid",
                        "attrs":{
                        }
                        }
                    }
                    }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries?locale={locale}")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")



    def test_update_entry(self):
        data = {
                    "entry": {
                        "title": "test 3",
                        "url": "/test3"
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_atomic_update_entry_with_push(self):
        data = {
                    "entry": {
                        "multiple_number": {
                            "PUSH": {
                                "data": [
                                    2,
                                    3
                                ]
                            }
                        },
                        "multiple_group": {
                            "PUSH": {
                                "data": {
                                    "demo_field": "abc"
                                }
                            }
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_atomic_update_entry_with_pull(self):
        data = {
                    "entry": {
                        "multiple_number": {
                            "PULL": {
                                "query": {
                                    "$in": [
                                        2,
                                        3
                                    ]
                                }
                            }
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_atomic_update_entry_with_update(self):
        data = {
                    "entry": {
                        "multiple_number": {
                            "UPDATE": {
                                "index": 0,
                                "data": 1
                            }
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_atomic_update_entry_with_add(self):
        data = {
                    "entry": {
                        "number": {
                            "ADD": 1
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_atomic_update_entry_with_sub(self):
        data ={
                    "entry": {
                        "number": {
                            "SUB": 2
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale={locale}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_entry_version_naming(self):
        data = {
                    "entry": {
                        "_version_name": "Test version",
                        "locale": "en-us",
                        "force": True
                    }
                }
        version_number = 1
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).version_naming(version_number, data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/versions/{version_number}/name")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_get_references(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).references()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/references")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.body, None)

    def test_get_languages(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).languages()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/locales")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_localize(self):
        data = {
                "entry": {
                    "title": "Home",
                    "url": "/home-french",
                    "tags": [],
                    "locale": "en-us",
                    "uid": "test-uid",
                    "created_by": "user-uid",
                    "updated_by": "user-uid",
                    "created_at": "2017-06-13T12:34:52.083Z",
                    "updated_at": "2018-12-28T06:33:06.752Z",
                    "ACL": {},
                    "_version": 2
                    }
            }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).localize(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?locale=en-us")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_unlocalize(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).unlocalize()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/unlocalize?locale=en-us")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}?force=True")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_imports(self):
        file_path = "tests/resources/imports/entry.json"
        response = self.client.stack(api_key).content_types(content_type_uid).entry().imports(file_path)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/import?locale=en-us")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "multipart/form-data")

    def test_exports(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).export()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/export")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_publish(self):
        data = {
                    "entry": {
                        "environments": ["development"],
                        "locales": ["en-us"]
                    },
                    "locale": "en-us",
                    "version": 1,
                    "scheduled_at": "2019-02-14T18:30:00.000Z"
                }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).publish(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/publish")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_unpublish(self):
        data = {
                    "entry": {
                        "environments": ["development"],
                        "locales": ["en-us"]
                    },
                    "locale": "en-us",
                    "version": 1,
                    "scheduled_at": "2019-02-14T18:30:00.000Z"
                }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).unpublish(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/unpublish")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    


if __name__ == '__main__':
    unittest.main()
