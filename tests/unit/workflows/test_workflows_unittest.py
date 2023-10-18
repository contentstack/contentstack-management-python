import os
import unittest
from dotenv import load_dotenv
import contentstack_management
from tests.cred import get_credentials

credentials = get_credentials()
username = credentials["username"]
password = credentials["password"]
host = credentials["host"]
api_key = credentials["api_key"]
workflow_uid = credentials["workflow_uid"]
content_type_uid = credentials["content_type_uid"]
entry_uid = credentials["entry_uid"]
rule_uid = credentials["rule_uid"]



class WorkflowsUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = contentstack_management.Client(host=host)
        self.client.login(username, password)

    def test_get_all_workflows(self):
        response = self.client.stack(api_key).workflows().find()
        self.assertEqual(response.request.url, f"{self.client.endpoint}workflows")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_get_a_workflows(self):
        response = self.client.stack(api_key).workflows(workflow_uid).fetch()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/{workflow_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_create(self):
        data = {
                "workflow":{
                    "workflow_stages":[
                        {
                            "color":"#2196f3",
                            "SYS_ACL":{
                                "roles":{
                                    "uids":[
                                        
                                    ]
                                },
                                "users":{
                                    "uids":[
                                        "$all"
                                    ]
                                },
                                "others":{
                                    
                                }
                            },
                            "next_available_stages":[
                                "$all"
                            ],
                            "allStages":True,
                            "allUsers":True,
                            "specificStages":False,
                            "specificUsers":False,
                            "entry_lock":"$none",
                            "name":"Review"
                        },
                        {
                            "color":"#74ba76",
                            "SYS_ACL":{
                                "roles":{
                                    "uids":[
                                        
                                    ]
                                },
                                "users":{
                                    "uids":[
                                        "$all"
                                    ]
                                },
                                "others":{
                                    
                                }
                            },
                            "allStages":True,
                            "allUsers":True,
                            "specificStages":False,
                            "specificUsers":False,
                            "next_available_stages":[
                                "$all"
                            ],
                            "entry_lock":"$none",
                            "name":"Complete"
                        }
                    ],
                    "admin_users":{
                        "users":[
                            
                        ]
                    },
                    "name":"Workflow",
                    "enabled":True,
                    "branches":[
                        "main",
                        "development"
                    ],
                    "content_types":[
                        "$all"
                    ]
                }
            }
        response = self.client.stack(api_key).workflows().create(data)
        self.assertEqual(response.request.url, f"{self.client.endpoint}workflows")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_workflows(self):
        data = {
                "workflow":{
                    "workflow_stages":[
                        {
                            "color":"#2196f3",
                            "SYS_ACL":{
                                "roles":{
                                    "uids":[
                                        
                                    ]
                                },
                                "users":{
                                    "uids":[
                                        "$all"
                                    ]
                                },
                                "others":{
                                    
                                }
                            },
                            "next_available_stages":[
                                "$all"
                            ],
                            "allStages":True,
                            "allUsers":True,
                            "specificStages":False,
                            "specificUsers":False,
                            "entry_lock":"$none",
                            "name":"Review"
                        },
                        {
                            "color":"#74ba76",
                            "SYS_ACL":{
                                "roles":{
                                    "uids":[
                                        
                                    ]
                                },
                                "users":{
                                    "uids":[
                                        "$all"
                                    ]
                                },
                                "others":{
                                    
                                }
                            },
                            "allStages":True,
                            "allUsers":True,
                            "specificStages":False,
                            "specificUsers":False,
                            "next_available_stages":[
                                "$all"
                            ],
                            "entry_lock":"$none",
                            "name":"Complete"
                        }
                    ],
                    "admin_users":{
                        "users":[
                            
                        ]
                    },
                    "name":"Workflow",
                    "enabled":True,
                    "branches":[
                        "main",
                        "development"
                    ],
                    "content_types":[
                        "$all"
                    ]
                }
                }
        response = self.client.stack(api_key).workflows(workflow_uid).update(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/{workflow_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")


    def test_delete_workflows(self):
        response = self.client.stack(api_key).workflows(workflow_uid).delete()
        self.assertEqual(response.request.url, f"{self.client.endpoint}workflows/{workflow_uid}")
        self.assertEqual(response.request.method, "DELETE")

    def test_enable(self):
        response = self.client.stack(api_key).workflows(workflow_uid).enable()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/{workflow_uid}/enable")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_disable(self):
        response = self.client.stack(api_key).workflows(workflow_uid).disable()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/{workflow_uid}/disable")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_set_workflow_stage(self):
        data = {
                "workflow": {
                    "workflow_stage": {
                        "comment": "Workflow Comment",
                        "due_date": "Thu Dec 01 2018",
                        "notify": False,
                        "uid": "workflow_stage_uid",
                        "assigned_to": [{
                                "uid": "user_uid", 
                                "name": "Username", 
                                "email": "user_email_id"
                                }],
                        "assigned_by_roles": [{
                            "uid": "role_uid",
                            "name": "Role name"
                        }]		
                    }
                }
            }
        response = self.client.stack(api_key).workflows().set_workflow_stage(content_type_uid, entry_uid, data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/workflow")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_create_publish_rule(self):
        data = {
                    "publishing_rule":{
                        "workflow":"workflow_uid",
                        "actions":[],
                        "branches":[
                            "main",
                            "development"
                        ],
                        "content_types":[
                            "$all"
                        ],
                        "locales":[
                            "en-us"
                        ],
                        "environment":"environment_uid",
                        "approvers":{
                            "users":[
                                "user_uids"
                            ],
                            "roles":[
                                "role_uids"
                            ]
                        },
                        "workflow_stage":"workflow_stage_uid",
                        "disable_approver_publishing":False
                    }
                }
        response = self.client.stack(api_key).workflows(workflow_uid).create_publish_rule(data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/publishing_rules")
        self.assertEqual(response.request.method, "POST")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_update_publish_rule(self):
        data = {
                    "publishing_rule": {
                        "workflow": "workflow_uid",
                        "actions": [],
                        "branches": [
                            "main",
                            "development"
                        ],
                        "content_types": ["$all"],
                        "locales": ["en-us"],
                        "environment": "environment_uid",
                        "approvers": {
                            "users": ["user_uid"],
                            "roles": ["role_uid"]
                        },
                        "workflow_stage": "workflow_stage_uid",
                        "disable_approver_publishing": False

                    }
                }

        response = self.client.stack(api_key).workflows(workflow_uid).update_publish_rule(rule_uid, data)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/publishing_rules/{rule_uid}")
        self.assertEqual(response.request.method, "PUT")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_delete_publish_rule(self):
        response = self.client.stack(api_key).workflows(workflow_uid).delete_publish_rule(rule_uid)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/publishing_rules/{rule_uid}")
        self.assertEqual(response.request.method, "DELETE")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_fetch_publish_rule(self):
        response = self.client.stack(api_key).workflows(workflow_uid).fetch_publish_rule(rule_uid)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/publishing_rules/{rule_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")

    def test_fetch_publish_rules(self):
        response = self.client.stack(api_key).workflows(workflow_uid).fetch_publish_rules()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/publishing_rules")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_publish_rule_content_type(self):
        response = self.client.stack(api_key).workflows().fetch_publish_rule_content_type(content_type_uid)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}workflows/content_type/{content_type_uid}")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_publish_request_approval(self):
        response = self.client.stack(api_key).workflows(workflow_uid).publish_request_approval(content_type_uid, entry_uid)
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}content_types/{content_type_uid}/entries/{entry_uid}/workflow")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    def test_fetch_tasks(self):
        response = self.client.stack(api_key).workflows().fetch_tasks()
        self.assertEqual(response.request.url,
                         f"{self.client.endpoint}user/assignments")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.headers["Content-Type"], "application/json")
        self.assertEqual(response.request.body, None)

    


