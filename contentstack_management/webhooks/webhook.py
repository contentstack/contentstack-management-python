"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote

class Webhook(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, webhook_uid):
        self.client = client
        self.webhook_uid = webhook_uid
        super().__init__(self.client)

        self.path = f"webhooks"

    def find(self):
        """
        The Get all Webhooks request returns comprehensive information on all the available webhooks in the specified stack
        :return: the result of a GET request to the specified URL, using the headers specified in the
        client object.The URL being used for the API call is "webhooks". The headers and parameters
        for the API call are being passed as arguments to the `get` method. The result of the API call
        is being returned.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack("api_key").webhooks().find().json()

        -------------------------------
        """
        
        
        url = self.path
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The `Get webhook` request returns comprehensive information on a specific webhook.
        :return: The fetch method returns the response from the Get an webhook request, which contains
        comprehensive information about a specific version of an webhook of a stack.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks('webhook_uid').fetch().json()

        -------------------------------
        """
        if self.webhook_uid is None:
            raise Exception('Webhook uid is required')
        url = f"{self.path}/{self.webhook_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def create(self, data):
        """
        The Create a webhook request allows you to create a new webhook in a specific stack.
        
        :param data: In the `data` section, you need to enter the name of the webhook; the destination details i.e.,
        target urls, basic authentication details, and custom headers; 
        and the channels; and set the disabled and concise_payload parameters as per requirement.
        
        :return: Json, with webhook details.

        -------------------------------
        [Example:]
            >>> data = {
            >>>            "webhook":{
            >>>                "name":"Test",
            >>>                "destinations":[
            >>>                {
            >>>                    "target_url":"http://example.com",
            >>>                    "http_basic_auth":"basic",
            >>>                    "http_basic_password":"test",
            >>>                    "custom_header":[
            >>>                    {
            >>>                        "header_name":"Custom",
            >>>                        "value":"testing"
            >>>                    }
            >>>                    ]
            >>>                }
            >>>                ],
            >>>                "notifiers": "dave.joe@gmail.com",
            >>>                "channels":[
            >>>                "assets.create"
            >>>                ],
            >>>                "branches":[
            >>>                "main"
            >>>                ],
            >>>                "retry_policy":"manual",
            >>>                "disabled":false,
            >>>                "concise_payload":true
            >>>            }
            >>>            }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks().create(data).json()

        -------------------------------
        """
        
        
        data = json.dumps(data)
        return self.client.post(self.path, headers = self.client.headers, data=data, params = self.params)
    
    def update(self, data):
        """
        The Update webhook request allows you to update the details of an existing webhook in the stack.
        
        :param data: In the data section, you need to enter new details such as the name of the webhook; the destination details 
        i.e., target urls, basic authentication details, and custom headers; and the channels; or reset the disabled or concise_payload parameters as per requirement
        :return: Json, with updated webhook details.
        -------------------------------
        [Example:]
            >>> 
            >>> data = {
            >>>         "webhook":{
            >>>             "name":"Updated webhook",
            >>>             "destinations":[
            >>>             {
            >>>                 "target_url":"http://example.com",
            >>>                 "http_basic_auth":"basic",
            >>>                 "http_basic_password":"test",
            >>>                 "custom_header":[
            >>>                 {
            >>>                     "header_name":"Custom",
            >>>                     "value":"testing"
            >>>                 }
            >>>                 ]
            >>>             }
            >>>             ],
            >>>             "channels":[
            >>>             "assets.create"
            >>>             ],
            >>>             "branches":[
            >>>             "main"
            >>>             ],
            >>>             "retry_policy":"manual",
            >>>             "disabled":true,
            >>>             "concise_payload":true
            >>>         }
            >>>         }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks('webhook_uid').update(data).json()

        -------------------------------
        """
        
        if self.webhook_uid is None:
            raise Exception('Webhook uid is required')
        url = f"{self.path}/{self.webhook_uid}"
        data = json.dumps(data)
        return self.client.put(url, headers = self.client.headers, data=data, params = self.params)
    
    
    def delete(self): 
        """
        The Delete webhook call deletes an existing webhook from a stack.
        :return: The delete() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = result = client.stack('api_key').webhooks('webhook_uid').delete().json()

        -------------------------------
        """
        
        
        if self.webhook_uid is None:
            raise Exception('Webhook uid is required')
        if self.client.headers['Content-Type'] is not None:
            self.client.headers.pop('Content-Type')
        url = f"{self.path}/{self.webhook_uid}"
        
        return self.client.delete(url, headers = self.client.headers, params = self.params)
    
    def imports(self, file_path):
        """
        The 'Import Webhook' section consists of the following two requests that will help you to 
        import new Webhooks or update existing ones by uploading JSON files.
        
        :param file_path: The `file_path` parameter is a string that represents the path to the file
        that you want to import. It should be the absolute or relative path to the file on your local
        machine
        :return: The imports() method returns the status code and message as a response.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> file_path = "tests/resources/mock_content_types/import_content_types.json"
            >>> result = client.stack('api_key').webhooks().imports(file_path).json()

        -------------------------------
        """
        
        if file_path is None:
            raise Exception('File path is required')
        url = f"{self.path}/import"
        self.client.headers['Content-Type'] = "multipart/form-data"
        files = {'entry': open(f"{file_path}",'rb')}
        return self.client.post(url, headers = self.client.headers, files = files, params = self.params)
    
    def export(self):
        """
        The Export a Webhook request exports an existing webhook. 
        The exported webhook data is saved in a downloadable JSON file. 
        The exported file won't get downloaded automatically. 
        To download the exported file, a REST API client, such as Postman can be used.
        :return: Json, with webhook details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks('webhook_uid').export().json()

        -------------------------------
        """
        
        if self.webhook_uid is None:
            raise Exception('Webhok uid is required')
        url = f"{self.path}/{self.webhook_uid}/export"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def executions(self):
        """
        The Get executions of a webhook request allows you to fetch the execution details of a specific webhook, 
        which includes the execution UID. These details are instrumental in retrieving webhook logs and retrying a failed webhook.
        :return: Json, with webhook details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks('webhook_execution_uid').executions().json()

        -------------------------------
        """
        
        if self.webhook_uid is None:
            raise Exception('Webhook uid is required')
        url = f"{self.path}/{self.webhook_uid}/executions"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    def retry(self, execution_uid):
        """
        This call makes a manual attempt to execute a webhook after the webhook has finished executing its automatic attempts.
        
        :param execution_uid: The `execution_uid` parameter is a unique identifier for a specific
        execution. It is used to identify which execution should be retried
        :return: Json, with webhook details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks().retry('execution_uid').json()

        -------------------------------
        """
        
        if execution_uid is None:
            raise Exception('Execution uid is required')
        url = f"{self.path}/{execution_uid}/retry"
        return self.client.post(url, headers = self.client.headers, params = self.params)
    
    
    
    def logs(self, execution_uid):
        """
        Get latest execution log of a webhook call will return a comprehensive detail of all the webhooks
        that were executed at a particular execution cycle.
        
        :param execution_uid: The `execution_uid` parameter is a unique identifier for a specific
        execution. It is used to identify which execution should be retried
        :return: Json, with webhook details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack('api_key').webhooks().logs('execution_uid').json()

        -------------------------------
        """
        if execution_uid is None:
            raise Exception('Execution uid is required')
        url = f"{self.path}/{execution_uid}/logs"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    

    

    


