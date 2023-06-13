"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import requests
import json
from ..organizations.organizations import Organization
from ..users.user import User
from ..stack.stack import Stack
from ..user_session.user_session import UserSession

class ApiClient:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint, host, headers, authtoken, authorization, failure_retry, exceptions: bool,
                 errors: bool, timeout: int, max_requests: int, retry_on_error: bool):
        self.authorization = authorization
        self.authtoken = authtoken
        self.headers = headers
        self.host = host
        self.endpoint = endpoint
        self.failure_retry = failure_retry
        self.exceptions = exceptions
        self.errors = errors
        self.timeout = timeout
        self.max_requests = max_requests
        self.retry_on_error = retry_on_error


    def get(self, url, headers=None, params=None):
        """
        Perform an HTTP GET request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :return: The response from the server.
        """
        return self._call_request('GET', url, headers=headers, params=params)

    def put(self, url, headers=None, params=None, data=None, json_data=None):

        """
        Perform an HTTP PUT request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :param data: Optional dictionary, list of tuples, or bytes to include in the body of the request.
        :param json: Optional JSON data to include in the body of the request.
        :return: The response from the server.
        """
        return self._call_request('PUT', url, headers=headers, params=params, data=data, json_data=json)

    def post(self, url, headers=None, params=None, data=None, json_data=None, files=None):

        """
        Perform an HTTP POST request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :param data: Optional dictionary, list of tuples, or bytes to include in the body of the request.
        :param json: Optional JSON data to include in the body of the request.
        :return: The response from the server.
        """
        return self._call_request('POST', url, headers=headers, params=params, data=data, json_data=json_data, files=files)


    def delete(self, url, headers=None, params=None):
        """
        Perform an HTTP DELETE request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :return: The response from the server.
        """
        return self._call_request('DELETE', url, headers=headers, params=params)
    

    
    def _call_request(self, method, url_path, headers=None, params=None, data=None, json_data=None, files=None):

        url = f"{self.endpoint}/{url_path}"
        retries = self.failure_retry + 1

        while retries > 0:
            try:
                response = requests.request(method, url, data=data, headers=headers, params=params, json=json_data, files=files)
                if response.status_code >= 400:
                    if self.errors:
                        return response

                    elif retries > 1:
                        retries -= 1
                    else:
                        return None
                else:
                    return response

            except Exception as e:
                if self.exceptions:
                    raise e
                elif retries > 1:
                    retries -= 1
                else:
                    return None

    def login(self,  email=None, password=None):
        """
        Fetches the user details and logging into the stack
        :return: User details, fetch authtoken.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> response = client.login(email="email_id", password="password")
        -------------------------------
        """

        self.api_client = ApiClient(
                    host=self.host, endpoint=self.endpoint, authtoken=self.authtoken,
                     headers=self.headers, authorization=self.authorization,
                     timeout=self.timeout, failure_retry=self.failure_retry, exceptions=self.exceptions, errors=self.errors,
                     max_requests=self.max_requests, retry_on_error=self.retry_on_error
        )
        response = UserSession(username=email, password= password, api_client=self.api_client).login()
        self.auth_token = self.get_authtoken(response.json())  if response.status_code == 200 else self.authtoken 
        return response
    

       
    def logout(self):
        """
        Logging out from the stack
        :return: Json, with status code and message.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> response = client.logout()
        -------------------------------
        """
        return UserSession(api_client = self.api_client).logout()

    def get_authtoken(self, response):
        """
        Fetches the authtoken from the successful response
        :return: Text, Auth token.
        -------------------------------
        [Example:]

            >>> from contentstack_management import contentstack
            >>> client = contentstack.client(host='HOST NAME')
            >>> response = client.login(email="email_id", password="password").json()
            >>> auth_token = client.get_authtoken(response)
        -------------------------------
        """
        return response['user']['authtoken']      
    
    def user(self):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client)
        
    def organizations(self, organization_uid = None):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client, organization_uid)
    
    def stack(self, api_key = None):
        return Stack(self.endpoint, self.auth_token, self.headers,self.api_client, api_key)
    

