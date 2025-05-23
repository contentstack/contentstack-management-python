import json
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

def read_file(self, file_name):
	file_path = f"tests/resources/mock_entries/{file_name}"
	infile = open(file_path, 'r')
	data = infile.read()
	infile.close()
	return data

class EntryMockTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_entries(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry().find().json()
        read_mock_entry_data = read_file("get_all.json")
        mock_entry_data = json.loads(read_mock_entry_data)
        self.assertEqual(mock_entry_data.keys(), response.keys())


    def test_get_a_entry(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry().fetch().json()
        self.assertEqual(entry_uid, response["entries"]["uid"])

        
    def test_create(self):
        data = {
                    "entry": {
                        "title": "example",
                        "url": "/example"
                    }
                }
        response = self.client.stack(api_key).content_types(content_type_uid).entry().create(data).json()
        self.assertEqual("Entry created successfully.", response['notice'])


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
        response = self.client.stack(api_key).content_types(content_type_uid).entry().create(data).json()
        self.assertEqual("Entry created successfully.", response['notice'])




    def test_update_entry(self):
        data = {
                    "entry": {
                        "title": "test 3",
                        "url": "/test3"
                    }
                }
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])


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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])

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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])

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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])

    def test_atomic_update_entry_with_add(self):
        data = {
                    "entry": {
                        "number": {
                            "ADD": 1
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])


    def test_atomic_update_entry_with_sub(self):
        data ={
                    "entry": {
                        "number": {
                            "SUB": 2
                        }
                    }
                }
        locale = "en-us"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).update(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])



    def test_entry_version_naming(self):
        data = {
                    "entry": {
                        "_version_name": "Test version",
                        "locale": "en-us",
                        "force": True
                    }
                }
        version_number = 1
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).version_naming(version_number, data).json()
        self.assertEqual("Version name assigned successfully", response['notice'])


    def test_get_references(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).references().json()
        self.assertEqual(response['references'], not None)

    def test_get_languages(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).languages().json()
        self.assertEqual("en-us", response['locales'][0]['code'])

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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).localize(data).json()
        self.assertEqual("Entry updated successfully.", response['notice'])

    def test_unlocalize(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).unlocalize().json()
        self.assertEqual(response['locale'], not None)

    def test_delete(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).delete().json()
        self.assertEqual("Entry deleted successfully.", response['notice'])

    def test_imports(self):
        file_path = "/Downloads/entry.json"
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).imports(file_path).json()
        self.assertEqual(response.request.url, f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/import?locale=en-us")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "multipart/form-data")

    def test_exports(self):
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).export().json()
        read_mock_entry_data = read_file("export.json")
        mock_entry_data = json.loads(read_mock_entry_data)
        self.assertEqual(mock_entry_data.keys(), response.keys())

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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).publish(data).json()
        self.assertEqual("The requested action has been performed.", response['notice'])

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
        response = self.client.stack(api_key).content_types(content_type_uid).entry(entry_uid).unpublish(data).json()
        self.assertEqual("The requested action has been performed.", response['notice'])

if __name__ == '__main__':
    unittest.main()
