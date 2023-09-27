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


class bulk_operationMockTests(unittest.TestCase):

    def setUp(self):
        
        self.client = contentstack.ContentstackClient(host = host)
        self.client.login(username, password)

    def test_publish(self):
        data = {
                "entries":[
                    {
                        "uid":"entry_uid",
                        "content_type":"ct0",
                        "version":"5",
                        "locale":"en-us"
                    },
                    {
                        "uid":"entry_uid",
                        "content_type":"ct0",
                        "version":"1",
                        "locale":"en-us"
                    },
                    {
                        "uid":"entry_uid",
                        "content_type":"ct5",
                        "version":"2",
                        "locale":"en-us"
                    }
                ],
                "locales":[
                    "en-us"
                ],
                "environments":[
                    "env1"
                ],
                "rules":{
                    "approvals":"true/false"
                },
                "scheduled_at":"scheduled_time",
                "publish_with_reference":True
                }

        response = self.client.stack(api_key).bulk_operation().publish(data).json()
        self.assertEqual("Your bulk publish request is in progress. Please check publish queue for more details.", response['notice'])

    def test_unpublish(self):
        data = {
                "entries": [
                    {
                    "content_type": "news",
                    "uid": "entry_uid",
                    "locale": "en-us"
                    },
                    {
                    "content_type": "article",
                    "uid": "entry_uid",
                    "locale": "en-us"
                    }
                ],
                "workflow": {
                    "workflow_stage": {
                    "comment": "String Comment",
                    "due_date": "Thu Dec 01 2018",
                    "notify": False,
                    "uid": "workflow_stage_uid",
                    "assigned_to": [
                        {
                        "uid": "user_uid",
                        "name": "user_name",
                        "email": "user_email_ID"
                        }
                    ],
                    "assigned_by_roles": [
                        {
                        "uid": "user_uid",
                        "name": "Content Manager"
                        }
                    ]
                    }
                },
                "locales": [
                    "en-us"
                ],
                "environments": [
                    "env_uid"
                ]
                }
        response = self.client.stack(api_key).bulk_operation().unpublish(data).json()
        self.assertEqual("Your bulk unpublish request is in progress. Please check publish queue for more details.", response['notice'])

    def test_update(self):
        data = {
                "entries": [{
                    "content_type": "content_type_uid1",
                    "uid": "entry_uid",
                    "locale": "en-us"
                }, {
                    "content_type": "content_type_uid2",
                    "uid": "entry_uid",
                    "locale": "en-us"
                }],
                "workflow": {
                    "workflow_stage": {
                        "comment": "Workflow-related Comments",
                        "due_date": "Thu Dec 01 2018",
                        "notify": False,
                        "uid": "workflow_stage_uid",
                        "assigned_to": [{
                            "uid": "user_uid",
                            "name": "user_name",
                            "email": "user_email_id"
                        }],
                        "assigned_by_roles": [{
                            "uid": "role_uid",
                            "name": "role_name"
                        }]
                    }
                }
            }
        response = self.client.stack(api_key).bulk_operation().update(data).json()
        self.assertEqual("Your bulk workflow update request is in progress. Please check publish queue for more details.", response['notice'])

    def test_delete(self):
        data = {
                "entries":[{
                    "content_type":"content_type_uid",
                    "uid":"entry_uid",
                    "locale":"locale"
                },{
                    "content_type":"content_type_uid",
                    "uid":"entry_uid",
                    "locale":"entry_locale"
                }
                ],
                "assets": [{
                    "uid": "uid"
                }]
            }
        response = self.client.stack(api_key).bulk_operation().delete(data).json()
        self.assertEqual("Your bulk delete request is in progress. Please check publish queue for more details.", response['notice'])
        

    
