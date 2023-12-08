"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote

class Workflows(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, workflow_uid):
        self.client = client
        self.workflow_uid = workflow_uid
        super().__init__(self.client)

        self.path = f"workflows"

    def find(self):
        """
        The Get all Workflows request retrieves the details of all the Workflows of a stack.
        :return: the result of a GET request to the specified URL, using the headers specified in the
        client object.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack("api_key").workflows().find().json()

        -------------------------------
        """        
        url = self.path
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The Get a Single Workflow request retrieves the comprehensive details of a specific Workflow of a stack.
        :return: The fetch method returns the response from the Get an workflow request, which contains
        comprehensive information about a specific version of an workflow of a stack.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows('workflow_uid').fetch().json()

        -------------------------------
        """
        if self.workflow_uid is None:
            raise Exception('workflow uid is required')
        url = f"{self.path}/{self.workflow_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data):
        """
        The Create a Workflow request allows you to create a Workflow.

        :param data: The data parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with workflow details.

        -------------------------------
        [Example:]
            >>> data = {
            >>>        "workflow":{
            >>>            "workflow_stages":[
            >>>                {
            >>>                    "color":"#2196f3",
            >>>                    "SYS_ACL":{
            >>>                        "roles":{
            >>>                            "uids":[
            >>>                            ]
            >>>                        },
            >>>                        "users":{
            >>>                            "uids":[
            >>>                                "$all"
            >>>                            ]
            >>>                        },
            >>>                        "others":{
            >>>                        }
            >>>                    },
            >>>                    "next_available_stages":[
            >>>                        "$all"
            >>>                    ],
            >>>                    "allStages":true,
            >>>                    "allUsers":true,
            >>>                    "specificStages":false,
            >>>                    "specificUsers":false,
            >>>                    "entry_lock":"$none",
            >>>                    "name":"Review"
            >>>                },
            >>>                {
            >>>                    "color":"#74ba76",
            >>>                    "SYS_ACL":{
            >>>                        "roles":{
            >>>                            "uids":[
            >>>                            ]
            >>>                        },
            >>>                        "users":{
            >>>                            "uids":[
            >>>                                "$all"
            >>>                            ]
            >>>                        },
            >>>                        "others":{
            >>>                        }
            >>>                    },
            >>>                    "allStages":true,
            >>>                    "allUsers":true,
            >>>                    "specificStages":false,
            >>>                    "specificUsers":false,
            >>>                    "next_available_stages":[
            >>>                        "$all"
            >>>                    ],
            >>>                    "entry_lock":"$none",
            >>>                    "name":"Complete"
            >>>                }
            >>>            ],
            >>>            "admin_users":{
            >>>                "users":[
            >>>                ]
            >>>            },
            >>>            "name":"Workflow",
            >>>            "enabled":true,
            >>>            "branches":[
            >>>                "main",
            >>>                "development"
            >>>            ],
            >>>            "content_types":[
            >>>                "$all"
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().create(data).json()

        -------------------------------
        """
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data):
        """
        The Add or Update Workflow request allows you to add a workflow stage or update the details of the existing stages of a workflow.

        :param data: The `data` parameter is the data that you want to update. It should be a dictionary
        or an object that can be serialized to JSON
        :return: Json, with updated workflow details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "workflow":{
            >>>            "workflow_stages":[
            >>>                {
            >>>                    "color":"#2196f3",
            >>>                    "SYS_ACL":{
            >>>                        "roles":{
            >>>                            "uids":[
            >>>                            ]
            >>>                        },
            >>>                        "users":{
            >>>                            "uids":[
            >>>                                "$all"
            >>>                            ]
            >>>                        },
            >>>                        "others":{
            >>>                        }
            >>>                    },
            >>>                    "next_available_stages":[
            >>>                        "$all"
            >>>                    ],
            >>>                    "allStages":true,
            >>>                    "allUsers":true,
            >>>                    "specificStages":false,
            >>>                    "specificUsers":false,
            >>>                    "entry_lock":"$none",
            >>>                    "name":"Review"
            >>>                },
            >>>                {
            >>>                    "color":"#74ba76",
            >>>                    "SYS_ACL":{
            >>>                        "roles":{
            >>>                            "uids":[
            >>>                            ]
            >>>                        },
            >>>                        "users":{
            >>>                            "uids":[
            >>>                                "$all"
            >>>                            ]
            >>>                        },
            >>>                        "others":{
            >>>                        }
            >>>                    },
            >>>                    "allStages":true,
            >>>                    "allUsers":true,
            >>>                    "specificStages":false,
            >>>                    "specificUsers":false,
            >>>                    "next_available_stages":[
            >>>                        "$all"
            >>>                    ],
            >>>                    "entry_lock":"$none",
            >>>                    "name":"Complete"
            >>>                }
            >>>            ],
            >>>            "admin_users":{
            >>>                "users":[
            >>>                ]
            >>>            },
            >>>            "name":"Workflow",
            >>>            "enabled":true,
            >>>            "branches":[
            >>>                "main",
            >>>                "development"
            >>>            ],
            >>>            "content_types":[
            >>>                "$all"
            >>>            ]
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows("workflow_uid").update(data).json()
        -------------------------------
        
        """
        
        if self.workflow_uid is None:
            raise Exception('workflow uid is required')
        url = f"{self.path}/{self.workflow_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete Workflow request allows you to delete a workflow.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = result = client.stack('api_key').workflows('workflow_uid').delete().json()

        -------------------------------
        """
        
        
        if self.workflow_uid is None:
            raise Exception('workflow uid is required')
        url = f"{self.path}/{self.workflow_uid}"
        
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def disable(self):
        """
        The Disable Workflow request allows you to disable a workflow.
        
        :return: Json, with updated workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> file_path = "tests/resources/mock_content_types/import_content_types.json"
            >>> result = client.stack('api_key').workflows('workflow_uid').disable().json()

        -------------------------------
        """
        
        if self.workflow_uid is None:
            raise Exception('workflow uid is required')
        url = f"{self.path}/{self.workflow_uid}/disable"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def enable(self):
        """
        The Enable Workflow request allows you to enable a workflow. 
        :return: Json, with updated workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows('workflow_uid').export().json()

        -------------------------------
        """
        
        if self.workflow_uid is None:
            raise Exception('workflow uid is required')
        url = f"{self.path}/{self.workflow_uid}/enable"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def set_workflow_stage(self, content_type_uid, entry_uid, data):
        """
        The Set Entry Workflow Stage request allows you to either set a particular workflow stage of an entry or update the workflow stage details of an entry.
        
        :param content_type_uid: The content type uid is a unique identifier for a specific content type
        in your system. It helps identify the type of content you are working with
        :param entry_uid: The entry_uid parameter is the unique identifier of the entry that you want to
        set the workflow stage for
        :param data: The `data` parameter is a dictionary that contains the information needed to set
        the workflow stage for a specific entry. It should include the following key-value pairs:
        
        :return: Json, with workflow details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "workflow": {
            >>>            "workflow_stage": {
            >>>                "comment": "Workflow Comment",
            >>>                "due_date": "Thu Dec 01 2018",
            >>>                "notify": false,
            >>>                "uid": "workflow_stage_uid",
            >>>                "assigned_to": [{
            >>>                        "uid": "user_uid", 
            >>>                        "name": "Username", 
            >>>                        "email": "user_email_id"
            >>>                        }],
            >>>                "assigned_by_roles": [{
            >>>                    "uid": "role_uid",
            >>>                    "name": "Role name"
            >>>                }]		
            >>>            }
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().set_workflow_stage('content_type_uid', 'entry_uid', data).json()

        -------------------------------
        """
        
        
        if content_type_uid is None:
            raise Exception('Content type uid is required')
        if entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{content_type_uid}/entries/{entry_uid}/workflow"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    def create_publish_rule(self, data):
        """
        The Create Publish Rules request allows you to create publish rules for the workflow of a stack.

        :param data: The `data` parameter is a dictionary that contains the information needed to create
        a publishing rule. This dictionary should include the necessary fields such as the rule name,
        conditions, and actions. The exact structure of the `data` dictionary will depend on the
        requirements of the API you are using

        :return: Json, with workflow details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "publishing_rule":{
            >>>            "workflow":"workflow_uid",
            >>>            "actions":[],
            >>>            "branches":[
            >>>                "main",
            >>>                "development"
            >>>            ],
            >>>            "content_types":[
            >>>                "$all"
            >>>            ],
            >>>            "locales":[
            >>>                "en-us"
            >>>            ],
            >>>            "environment":"environment_uid",
            >>>            "approvers":{
            >>>                "users":[
            >>>                    "user_uids"
            >>>                ],
            >>>                "roles":[
            >>>                    "role_uids"
            >>>                ]
            >>>            },
            >>>            "workflow_stage":"workflow_stage_uid",
            >>>            "disable_approver_publishing":false
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().create_publish_rule(data).json()

        -------------------------------
        """
        
        
        url = f"{self.path}/publishing_rules"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params = self.params)
    
    
    
    def update_publish_rule(self, rule_uid, data):
        """
        The Update Publish Rules request allows you to add a publish rule or update the details of the existing publish rules of a workflow.
        
        :param rule_uid: The `rule_uid` parameter is the unique identifier of the publishing rule that
        you want to update
        :param data: The `data` parameter is a dictionary that contains the updated information for the
        publishing rule. It should include the fields and values that need to be updated for the rule
        :return: Json, with workflow details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>        "publishing_rule": {
            >>>            "workflow": "workflow_uid",
            >>>            "actions": [],
            >>>            "branches": [
            >>>                "main",
            >>>                "development"
            >>>            ],
            >>>            "content_types": ["$all"],
            >>>            "locales": ["en-us"],
            >>>            "environment": "environment_uid",
            >>>            "approvers": {
            >>>                "users": ["user_uid"],
            >>>                "roles": ["role_uid"]
            >>>            },
            >>>            "workflow_stage": "workflow_stage_uid",
            >>>            "disable_approver_publishing": false
            >>>        }
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().update_publish_rule('rule_uid', data).json()

        -------------------------------
        """
        
        if rule_uid is None:
            raise Exception('Rule uid is required')
        url = f"{self.path}/publishing_rules/{rule_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data = data, params = self.params)
    
    def delete_publish_rule(self, rule_uid):
        """
        The Delete Publish Rules request allows you to delete an existing publish rule. 
        
        :param rule_uid: The `rule_uid` parameter is the unique identifier of the publishing rule that
        you want to delete. It is used to specify which rule should be deleted from the system
        :return: the result of the `client.delete()` method, which is likely a response object or a
        boolean indicating the success of the deletion.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().delete_publish_rule('rule_uid').json()

        -------------------------------
        """
        
        if rule_uid is None:
            raise Exception('Rule uid is required')
        url = f"{self.path}/publishing_rules/{rule_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def fetch_publish_rule(self, rule_uid):
        """
       The Get a Single Publish Rule request retrieves the comprehensive details of a specific publish rule of a Workflow.
        
        :param rule_uid: The `rule_uid` parameter is the unique identifier of the publishing rule that
        you want to fetch. It is used to specify which rule you want to retrieve from the server
        :return: Json, with workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().fetch_publish_rule('rule_uid').json()

        -------------------------------
        """
        
        if rule_uid is None:
            raise Exception('Rule uid is required')
        url = f"{self.path}/publishing_rules/{rule_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def fetch_publish_rules(self):
        """
        The Get all Publish Rules request retrieves the details of all the Publish rules of a workflow. 
        :return: Json, with workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().fetch_publish_rules().json()

        -------------------------------
        """
        
        url = f"{self.path}/publishing_rules"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    

    def fetch_publish_rule_content_type(self, content_type_uid):
        """
        The Get Publish Rules by Content Types request allows you to retrieve details of a Publish Rule applied to a specific content type of your stack.
        
        :param content_type_uid: The `content_type_uid` parameter is a unique identifier for a specific
        content type. It is used to fetch the publish rule content type with the given identifier
        :return: Json, with workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().fetch_publish_rule_content_type('content_type_uid').json()

        -------------------------------
        """
        
        if content_type_uid is None:
            raise Exception('Content type uid is required')
        url = f"{self.path}/content_type/{content_type_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    

    def publish_request_approval(self, content_type_uid, entry_uid):
        """
        This multipurpose request allows you to either send a publish request or accept/reject a received publish request.
        
        :param content_type_uid: The content type uid is a unique identifier for a specific content type
        in your system. It is used to specify the type of content you are working with
        :param entry_uid: The entry_uid parameter is the unique identifier of the entry that you want to
        request approval for. It is used to specify which entry you want to perform the workflow action
        on
        :return: Json, with workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().publish_request_approval('content_type_uid', 'entry_uid').json()

        -------------------------------
        """
        
        if content_type_uid is None:
            raise Exception('Content type uid is required')
        if entry_uid is None:
            raise Exception('Entry uid is required')
        url = f"content_types/{content_type_uid}/entries/{entry_uid}/workflow"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    

    def fetch_tasks(self):
        """
        The Get all Tasks request retrieves a list of all tasks assigned to you.
        :return: Json, with workflow details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').workflows().logs().json()

        -------------------------------
        """
        url = f"user/assignments"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    

    

    


