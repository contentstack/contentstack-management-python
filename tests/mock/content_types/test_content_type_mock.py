import json
import os
import unittest

from dotenv import load_dotenv
from contentstack_management import contentstack
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
api_key = credentials["api_key"]
host = credentials["host"]
content_type_uid = credentials["content_type_uid"]

class ContentTypeMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_content_type/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_content_types(self):
        response = self.client.stack(api_key).content_type().find().json()
        read_mock_content_type_data  = self.read_file("find_content_types.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual(mock_content_type_data.keys(), response.keys())

    def test_get_a_content_type(self):
        response = self.client.stack(api_key).content_type(content_type_uid).fetch().json()
        read_mock_content_type_data  = self.read_file("fetch_a_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        uid = mock_content_type_data['content_type']['uid']
        self.assertEqual("content_type_get", uid)

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
        response = self.client.stack(api_key).content_type().create(data).json()
        read_mock_content_type_data  = self.read_file("create_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual("Content Type created successfully.", mock_content_type_data['notice'])

    def test_update_content_type(self):
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
        response = self.client.stack(api_key).content_type(content_type_uid).update(data).json
        read_mock_content_type_data  = self.read_file("update_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual("Content Type updated successfully.", mock_content_type_data['notice'])

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
        response = self.client.stack(api_key).content_type(content_type_uid).set_set_field_visibility_rules(data)
        read_mock_content_type_data  = self.read_file("set_field_visibility_rules.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual("Content Type updated successfully.", mock_content_type_data['notice'])

    def test_delete_content_type(self):
        response = self.client.stack(api_key).content_type(content_type_uid).delete().json()
        read_mock_content_type_data  = self.read_file("delete_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual("Content Type deleted successfully.", mock_content_type_data['notice'])
        
    def test_get_all_references(self):
        response = self.client.stack(api_key).content_type(content_type_uid).references().json()
        read_mock_content_type_data  = self.read_file("references_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual(mock_content_type_data.keys(), response.keys())

    def test_export(self):
        response = self.client.stack(api_key).content_type(content_type_uid).export().json()
        read_mock_content_type_data  = self.read_file("export_content_type.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual(mock_content_type_data.keys(), response.keys())

    def test_imports(self):
        file_path = "tests/resources/mock_content_type/import.json"
        response = self.client.stack(api_key).content_type().imports(file_path).json
        read_mock_content_type_data  = self.read_file("imports.json")
        mock_content_type_data = json.loads(read_mock_content_type_data)
        self.assertEqual("Content Type imported successfully.", mock_content_type_data['notice'])


if __name__ == '__main__':
    unittest.main()
