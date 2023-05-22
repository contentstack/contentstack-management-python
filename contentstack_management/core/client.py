"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import requests
import json


from ..organizations.organizations import Organization
from ..users.user import User
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

    def put(self, url, headers=None, params=None, data=None, json=None):
        """
        Perform an HTTP PUT request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :param data: Optional dictionary, list of tuples, or bytes to include in the body of the request.
        :param json: Optional JSON data to include in the body of the request.
        :return: The response from the server.
        """
        return self._call_request('PUT', url, headers=headers, params=params, data=data, json=json)

    def post(self, url, headers=None, params=None, data=None, json=None):
        """
        Perform an HTTP POST request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :param data: Optional dictionary, list of tuples, or bytes to include in the body of the request.
        :param json: Optional JSON data to include in the body of the request.
        :return: The response from the server.
        """
        return self._call_request('POST', url, headers=headers, params=params, data=data, json=json)

    def delete(self, url, headers=None, params=None):
        """
        Perform an HTTP DELETE request with the specified URL and parameters.

        :param url: The URL to send the request to.
        :param headers: Optional dictionary of headers to include in the request.
        :param params: Optional dictionary of URL parameters to include in the request.
        :return: The response from the server.
        """
        return self._call_request('DELETE', url, headers=headers, params=params)
    

    
    def _call_request(self, method, url_path, headers=None, params=None, data=None, json=None):
        url = f"{self.endpoint}/{url_path}"
        retries = self.failure_retry + 1

        while retries > 0:
            try:
                response = requests.request(method, url, data=data, headers=headers, params=params, json=json)

                if response.status_code >= 400:
                    if self.errors:
                        raise Exception(f"API returned an error: {response.text}")
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
                
    def login(self,  email, password):
        url = "user-session"
        data = {
            "user": {
                "email": email,
                "password": password

            }
        }
        data = json.dumps(data)
        self.api_client = ApiClient(
                    host=self.host, endpoint=self.endpoint, authtoken=self.authtoken,
                     headers=self.headers, authorization=self.authorization,
                     timeout=self.timeout, failure_retry=self.failure_retry, exceptions=self.exceptions, errors=self.errors,
                     max_requests=self.max_requests, retry_on_error=self.retry_on_error
        )

        response =  UserSession(url = url,headers = self.headers, data = data, api_client=self.api_client, endpoint=self.endpoint).login()
        self.auth_token = self.get_authtoken(response)
        return response
    
    def logout(self):
        url = "user-session"
        self.headers['authtoken'] = self.auth_token
        response =  UserSession(url = url,headers = self.headers, api_client = self.api_client, endpoint=self.endpoint).logout()
        return response
        
    def get_authtoken(self, response):
        return response['user']['authtoken']
        
    
    def get_user(self):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client).get_user()
    
    def update_user(self, user_data):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client).update_user(user_data)
    
    def active_user(self, user_activation_token, user_data):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client).update_user(user_activation_token, user_data)
    
    def request_password(self, user_data):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client).request_password(user_data)
    
    def reset_password(self, user_data):
        return User(self.endpoint, self.auth_token, self.headers,self.api_client).reset_password(user_data)
    
    def get_organizations(self):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).get_organizations()
    
    def get_organization(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).get_organizations(organization_uid)
    
    def get_organization_roles(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).get_organization_roles(organization_uid)
    
    def organization_add_users(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).organization_add_users(organization_uid)
    
    def transfer_organizations_onership(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).transfer_organizations_onership(organization_uid)
    
    def organization_stacks(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).organization_stacks(organization_uid)
    
    def organization_logs(self, organization_uid):
        return Organization(self.endpoint, self.auth_token, self.headers,self.api_client).organization_logs(organization_uid)
                
    
