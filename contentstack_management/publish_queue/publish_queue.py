"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from ..common import Parameter
from urllib.parse import quote
from .._errors import ArgumentException

class PublishQueue(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, publish_queue_uid: str):
        self.client = client
        self.publish_queue_uid = publish_queue_uid
        super().__init__(self.client)

        self.path = "publish-queue"

    def find(self):
        """
        The "Get publish queue" request returns comprehensive information on activities such as publish, unpublish, and delete performed on entries and/or assets. 
        This request also includes the details of the release deployments in the response body.
        :return: Json, with publish_queue details.

        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack("api_key").publish_queue().find().json()

        -------------------------------
        """        
        return self.client.get(self.path, headers = self.client.headers, params = self.params)
    
      
    
    def fetch(self):
        """
        The "Get publish queue activity" request returns comprehensive information on a specific publish, unpublish, or delete action performed on an entry and/or asset. You can also retrieve details of a specific release deployment.

        :return: Json, with publish_queue details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').publish_queue('publish_queue_uid').fetch().json()

        -------------------------------
        """
        self.validate_uid()
        url = f"{self.path}/{self.publish_queue_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)
        
    
    def cancel(self):
        """
        The "Cancel Scheduled Action" request will allow you to cancel any scheduled publishing or unpublishing activity of entries and/or assets and cancel the deployment of releases.

        :param data: The `data` parameter is the payload that you want to send in the request body. It
        should be a dictionary or a JSON serializable object that you want to send as the request body
        :return: Json, with publish_queue details.

        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').publish_queue().create(data).json()

        -------------------------------
        """
        
        self.validate_uid()
        url = f"{self.path}/{self.publish_queue_uid}/unschedule"
        return self.client.get(url, headers = self.client.headers, params = self.params)
    
    
    def validate_uid(self):
         if self.publish_queue_uid is None or '':
            raise ArgumentException("Publish Queue Uid is required")