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
workflow_uid = credentials["workflow_uid"]
content_type_uid = credentials["content_type_uid"]
entry_uid = credentials["entry_uid"]
rule_uid = credentials["rule_uid"]

class WorkflowsMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    
    def read_file(self, file_name):
        file_path= f"tests/resources/mock_workflows/{file_name}"
        infile = open(file_path, 'r')
        data = infile.read()
        infile.close()
        return data


    def test_get_all_workflows(self):
        response = self.client.stack(api_key).workflows().find().json()
        read_mock_workflows_data  = self.read_file("find.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_get_a_workflows(self):
        response = self.client.stack(api_key).workflows(workflow_uid).fetch().json()
        read_mock_workflows_data  = self.read_file("fetch.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_create(self):
        data ={
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
                            "main"
                        ],
                        "content_types":[
                            "$all"
                        ]
                    }
                }
        response = self.client.stack(api_key).workflows().create(data).json()
        read_mock_workflows_data  = self.read_file("create.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data['notice'], response["notice"])

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
        response = self.client.stack(api_key).workflows(workflow_uid).update(data).json()
        read_mock_workflows_data  = self.read_file("update.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual( mock_workflows_data['notice'], response['notice'])

    def test_delete_workflows(self):
        response = self.client.stack(api_key).workflows(workflow_uid).delete().json()
        read_mock_workflows_data  = self.read_file("delete.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data['notice'], response['notice'])
        

    def test_enable(self):
        response = self.client.stack(api_key).workflows(workflow_uid).enable().json()
        self.assertEqual("Workflow enabled successfully.", response['notice'])

    def test_disable(self):
        response = self.client.stack(api_key).workflows(workflow_uid).disable().json()
        self.assertEqual("Workflow disabled successfully.", response['notice'])

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
        response = self.client.stack(api_key).workflows().set_workflow_stage(content_type_uid, entry_uid, data).json()
        self.assertEqual("Workflow stage updated successfully.", response['notice'])

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
        response = self.client.stack(api_key).workflows().create_publish_rule(data).json()
        self.assertEqual("Publish rule created successfully." ,response['notice'])

    def test_update_publish_rule(self):
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
        response = self.client.stack(api_key).workflows().update_publish_rule(rule_uid, data).json()
        self.assertEqual("Publish rule updated successfully." ,response['notice'])

    def test_delete_publish_rule(self):
        response = self.client.stack(api_key).workflows().delete_publish_rule().json()
        self.assertEqual("Publish rule deleted successfully." ,response['notice'])

    def test_fetch_publish_rule(self):
        response = self.client.stack(api_key).workflows().fetch_publish_rule(rule_uid).json()
        read_mock_workflows_data  = self.read_file("publish_rule.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_fetch_publish_rules(self):
        response = self.client.stack(api_key).workflows().fetch_publish_rules().json()
        read_mock_workflows_data  = self.read_file("publish_rules.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_fetch_publish_rule_content_type(self):
        response = self.client.stack(api_key).workflows().fetch_publish_rule_content_type(content_type_uid).json()
        read_mock_workflows_data  = self.read_file("publish_rule_content_type.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_publish_request_approval(self):
        response = self.client.stack(api_key).workflows().publish_request_approval().json()
        read_mock_workflows_data  = self.read_file("retry.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())

    def test_fetch_tasks(self):
        response = self.client.stack(api_key).workflows().fetch_tasks().json()
        read_mock_workflows_data  = self.read_file("tasks.json")
        mock_workflows_data = json.loads(read_mock_workflows_data)
        self.assertEqual(mock_workflows_data.keys(), response.keys())


if __name__ == '__main__':
    unittest.main()
