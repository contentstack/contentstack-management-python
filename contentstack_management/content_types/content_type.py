"""Content type defines the structure or schema of a page or a section of your 
web or mobile property. To create content for your application, you are required 
to first create a content type, and then create entries using the content type. """

import json

class ContentType:
    """This class takes a base URL as an argument when it's initialized, 
        which is the endpoint for the RESTFUL API that we'll be interacting with.
        The create(), read(), update(), and delete() methods each correspond to 
        the CRUD operations that can be performed on the API"""

    def __init__(self, endpoint, authtoken, headers, api_client, api_key, authorization, branch, content_type_uid):
        self.api_client = api_client
        self.endpoint =  endpoint
        self.api_key = api_key
        self.params = {}
        self.headers = headers
        self.authtoken = authtoken
        self.authorization = authorization
        self.branch = branch
        self.content_type_uid = content_type_uid

    def find(self):
        r"""
        The Get all content types call returns comprehensive information of all the content 
        types available in a particular stack in your account.

        :return: Json, with all the content types details
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type()
            >>> response = content_type.find()
        --------------------------------
        """
        self.params = {
            "include_count": "false",
            "include_global_field_schema": "true",
            "include_branch": "false"
        }
        url = "content_types"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.get(url, headers = self.headers, params = self.params)
    
    def fetch(self):
        r"""
        The Get a single content type call returns information of a specific content type.

        :return: Json, with a single content type details
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.fetch()
        --------------------------------
        """
        self.params = {
            "version": 1,
            "include_global_field_schema": "true",
            "include_branch": "false"
        }
        url = f"content_types/{self.content_type_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.get(url, headers = self.headers, params = self.params)
    
    def create(self, data):
        r"""
        The Create a content type call creates a new content type 
        in a particular stack of your Contentstack account.

        :return: creates a content type with the given data
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> data = {
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
            >>> content_type = client.stack(api_key='api_key').content_type()
            >>> response = content_type.create(data)
        --------------------------------
        """

        self.params = {
            "include_branch": "false"
        }
        data = json.dumps(data)
        url = f"content_types"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.post(url, headers = self.headers, params = self.params, data = data)

    def update(self, data):
        r"""
        The Update Content Type call is used to update the schema of an existing content type.

        :return: Json, updates with all the content types details given
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> data = {
		            "content_type": {
		            	"title": "updated content type",
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
            >>> content_type = client.stack(api_key='api_key').content_type("content_type_uid)
            >>> response = content_type.update(data)
        --------------------------------
        """
        self.params = {
            "include_branch": "false"
        }
        data = json.dumps(data)
        url = f"content_types/{self.content_type_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.put(url, headers = self.headers, params = self.params, data = data)
    
    def set_set_field_visibility_rules(self, data):
        r"""
        The Set Field Visibility Rule for Content Type API request lets you add 
        Field Visibility Rules to existing content types. These rules allow you 
        to show and hide fields based on the state or value of certain fields.

        :return: Json, with content types details
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> data = {
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
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.set.set_field_visibility_rules(data)
        --------------------------------
        """
        self.params = {
            "include_branch": "false"
        }
        data = json.dumps(data)
        url = f"content_types/{self.content_type_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.put(url, headers = self.headers, params = self.params, data = data)
    
    def delete(self):
        r"""
        The Delete Content Type call deletes an existing content type and all the entries within it.

        :returns: Json, with status code and message.
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.delete()
        --------------------------------
        """
        self.params = {
            "force": "true"
        }
        url = f"content_types/{self.content_type_uid}"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.delete(url, headers = self.headers, params = self.params)
    
    def references(self):
        r"""
        The Get all references of content type call will fetch all the content types 
        in which a specified content type is referenced.

        :returns: Json, with content type references
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.references()
        --------------------------------
        """
        self.params = {
            "include_global_fields": "true",
            "include_branch": "false"
        }
        url = f"content_types/{self.content_type_uid}/references"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.get(url, headers = self.headers, params = self.params)
    
    def export(self):
        r"""
        This call is used to export a specific content type and its schema. 
        The data is exported in JSON format. The exported file won't get downloaded a
        utomatically. To download the exported file, a REST API client, such as Postman can be used.

        :returns: Json, with content type details.
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.export()
        --------------------------------
        """
        self.params = {
            "version": 1,
            "include_branch": "false"
        }
        url = f"content_types/{self.content_type_uid}/export"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['branch'] = self.branch
        return self.api_client.get(url, headers = self.headers, params = self.params)
    
    def import_content_type(self, file_path):
        r"""
        The Import a content type call imports a content type into a stack by uploading JSON file.

        :returns: Json, with status code and message.
    
        --------------------------------

        [Example:]
            >>> import contentstack
            >>> from contentstack_management import contentstack
            >>> content_type = client.stack(api_key='api_key').content_type(content_type_uid)
            >>> response = content_type.import_content_type()
        --------------------------------
        """
        self.params = {
            "overwrite": "false",
            "include_branch": "false"
        }
        url = f"content_types/import"
        self.headers['api_key'] = self.api_key
        self.headers['authtoken'] = self.authtoken
        self.headers['management_token'] = self.authorization
        self.headers['Content-Type'] = "multipart/form-data"
        self.headers['branch'] = self.branch
        files = {'content_type': open(f"{file_path}",'rb')}
        return self.api_client.post(url, headers = self.headers, params = self.params, files = files)
