import os
import unittest

from dotenv import load_dotenv

from contentstack_management import contentstack


def load_api_keys():
    load_dotenv()


class ContentTypeApiTests(unittest.TestCase):

    def setUp(self):
        load_api_keys()
        host = os.getenv("HOST")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        self.client = contentstack.client(host = host)
        self.client.login(email, password)

    def test_get_all_content_types(self):
        response = self.client.stack(os.getenv("API_KEY")).content_types().find()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")

    def test_get_a_content_types(self):
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).fetch()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.request.method, "GET")
         
    def test_create_content_types(self):
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
        response = self.client.stack(os.getenv("API_KEY")).content_types().create(data)
        if response.status_code == 201:
            result_json = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Content Type created successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 4222)

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
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).update(data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Content Type updated successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 422)

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
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).set_set_field_visibility_rules(data)
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Content Type updated successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 422)

    def test_delete_content_types(self):
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).delete()
        if response.status_code == 200:
            result_json = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(result_json.get('notice'))
            self.assertEqual("Content Type deleted successfully.", result_json.get('notice'))
        else:
            self.assertEqual(response.status_code, 422)

    def test_get_all_references(self):
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).references()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)


    def test_export(self):
        content_type_uid = os.getenv("CONTENT_TYPE_UID")
        response = self.client.stack(os.getenv("API_KEY")).content_types(content_type_uid).export()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 422)

    def test_import(self):
        file_path = "tests/resources/mock_content_type/import.json"
        response = self.client.stack(os.getenv("API_KEY")).content_types().imports(file_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.url, f"{self.client.endpoint}/content_types/import?overwrite=false&include_branch=false")
        self.assertEqual(response.request.method, "POST")


if __name__ == '__main__':
    unittest.main()
