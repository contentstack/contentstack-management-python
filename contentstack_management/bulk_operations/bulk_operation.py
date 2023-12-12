"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class BulkOperation(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client):
        self.client = client
        super().__init__(self.client)
        self.path = "bulk"


    def publish(self, data: dict):
        """
        The Publish entries and assets in bulk request allows you to publish multiple entries and assets at the same time.
        
        :param data: The `data` parameter is a dictionary that contains the data to be published
        :type data: dict
        :return: The `publish` method is returning the result of the `post` request made by the
        `client.post` method.
        -------------------------------
            [Example:]
                >>> data = {
                >>>            "entries":[
                >>>                {
                >>>                    "uid":"entry_uid",
                >>>                    "content_type":"ct0",
                >>>                    "version":"5",
                >>>                    "locale":"en-us"
                >>>                },
                >>>                {
                >>>                    "uid":"entry_uid",
                >>>                    "content_type":"ct0",
                >>>                    "version":"1",
                >>>                    "locale":"en-us"
                >>>                },
                >>>                {
                >>>                    "uid":"entry_uid",
                >>>                    "content_type":"ct5",
                >>>                    "version":"2",
                >>>                    "locale":"en-us"
                >>>                }
                >>>            ],
                >>>            "locales":[
                >>>                "en-us"
                >>>            ],
                >>>            "environments":[
                >>>                "env1"
                >>>            ],
                >>>            "rules":{
                >>>                "approvals":"true/false"
                >>>            },
                >>>            "scheduled_at":"scheduled_time",
                >>>            "publish_with_reference":true
                >>>            }
                >>> import contentstack_management
                >>> client = contentstack_management.Client(authtoken='your_authtoken')
                >>> result = client.stack('api_key').bulk_operation().publish(data).json()

            -------------------------------
        """
        url = f"{self.path}/publish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params=self.params)
        
    def unpublish(self, data: dict):
        """
        The Unpublish entries and assets in bulk request allows you to unpublish multiple entries and assets at the same time.
        
        :param data: The `data` parameter is a dictionary that contains the information needed to
        unpublish a resource. The specific keys and values in the dictionary will depend on the
        requirements of the API you are using
        :type data: dict
        :return: The method is returning the result of the `post` request made to the specified URL.
        -------------------------------
            [Example:]
                >>> data = {
                >>>        "entries": [
                >>>            {
                >>>            "content_type": "news",
                >>>            "uid": "entry_uid",
                >>>            "locale": "en-us"
                >>>            },
                >>>            {
                >>>            "content_type": "article",
                >>>            "uid": "entry_uid",
                >>>            "locale": "en-us"
                >>>            }
                >>>        ],
                >>>        "workflow": {
                >>>            "workflow_stage": {
                >>>            "comment": "String Comment",
                >>>            "due_date": "Thu Dec 01 2018",
                >>>            "notify": false,
                >>>            "uid": "workflow_uid",
                >>>            "assigned_to": [
                >>>                {
                >>>                "uid": "user_uid",
                >>>                "name": "user_name",
                >>>                "email": "user_email_ID"
                >>>                }
                >>>            ],
                >>>            "assigned_by_roles": [
                >>>                {
                >>>                "uid": "role_uid",
                >>>                "name": "Content Manager"
                >>>                }
                >>>            ]
                >>>            }
                >>>        },
                >>>        "locales": [
                >>>            "en-us"
                >>>        ],
                >>>        "environments": [
                >>>            "env_uid"
                >>>        ]
                >>>        }
                >>> import contentstack_management
                >>> client = contentstack_management.Client(authtoken='your_authtoken')
                >>> result = client.stack('api_key').bulk_operation().unpublish(data).json()

        -------------------------------
        """
            
        url = f"{self.path}/unpublish"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params=self.params)
    
    def delete(self, data: dict):
        """
        The Delete entries and assets in bulk request allows you to delete multiple entries and assets at the same time.
        
        :param data: The `data` parameter is a dictionary that contains the information needed to delete
        or unpublish a resource. The specific contents of the dictionary will depend on the requirements
        of the API you are using
        :type data: dict
        :return: the result of the `post` request made to the specified URL.
        -------------------------------
            [Example:]
                >>> data = {
                >>>        "entries":[{
                >>>            "content_type":"content_type_uid",
                >>>            "uid":"entry_uid",
                >>>            "locale":"locale"
                >>>        },{
                >>>            "content_type":"content_type_uid",
                >>>            "uid":"entry_uid",
                >>>            "locale":"entry_locale"
                >>>        }
                >>>        ],
                >>>        "assets": [{
                >>>            "uid": "uid"
                >>>        }]
                >>>    }
                >>> import contentstack_management
                >>> client = contentstack_management.Client(authtoken='your_authtoken')
                >>> result = client.stack('api_key').bulk_operation().delete(data).json()

        -------------------------------
        """
            
        url = f"{self.path}/delete"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params=self.params)
    
    def update(self, data: dict):
        """
        The above function updates the bulk_operation of an object by sending a POST request to the specified
        URL with the provided data.
        
        :param data: The `data` parameter is a dictionary that contains the information to be updated.
        It is converted to a JSON string using the `json.dumps()` function before being sent in the
        request
        :type data: dict
        :return: the result of the `post` request made to the specified URL with the provided headers
        and data.
        -------------------------------
            [Example:]
                >>> data = {
                >>>        "entries": [{
                >>>            "content_type": "content_type_uid1",
                >>>            "uid": "entry_uid",
                >>>            "locale": "en-us"
                >>>        }, {
                >>>            "content_type": "content_type_uid2",
                >>>            "uid": "entry_uid",
                >>>            "locale": "en-us"
                >>>        }],
                >>>        "workflow": {
                >>>            "workflow_stage": {
                >>>                "comment": "Workflow-related Comments",
                >>>                "due_date": "Thu Dec 01 2018",
                >>>                "notify": false,
                >>>                "uid": "workflow_stage_uid",
                >>>                "assigned_to": [{
                >>>                    "uid": "user_uid",
                >>>                    "name": "user_name",
                >>>                    "email": "user_email_id"
                >>>                }],
                >>>                "assigned_by_roles": [{
                >>>                    "uid": "role_uid",
                >>>                    "name": "role_name"
                >>>                }]
                >>>            }
                >>>        }
                >>>    }
                >>> import contentstack_management
                >>> client = contentstack_management.Client(authtoken='your_authtoken')
                >>> result = client.stack('api_key').bulk_operation().update(data).json()

        -------------------------------
        """
        
        url = f"{self.path}/workflow"
        data = json.dumps(data)
        return self.client.post(url, headers = self.client.headers, data = data, params=self.params)
    
    