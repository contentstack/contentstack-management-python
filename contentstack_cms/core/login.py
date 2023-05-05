import json
from json import JSONDecodeError
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
from contentstack_cms.core.http_client import HttpClient
from contentstack_cms.stack.stacks import Stacks
import contentstack_cms


DEFAULT_HOST = 'cdn.contentstack.io'
DEFAULT_REGION = 'eu'
VERSION='v3'



class Login:

    def __init__(self, email, password):

        self.email = email
        self.password = password
        self.region = DEFAULT_REGION
        self.version = VERSION
        self.host = self.get_host()
        self.obj = HttpClient()
        self.login()
        

    def login(self):
        data = {
                "user": {
                    "email": self.email,
                    "password": self.password
                    
                }
            }
        headers = self.user_agents()
        url = f'{self.host}/user-session'
        response = self.obj.create_api(url, headers, data)
        self.auth_token = self.get_authtoken(response)
        return response



    def get_authtoken_by_email_password(self, email, password):
        data = {
                "user": {
                    "email": email,
                    "password": password
                    
                }
            }
        headers = self.user_agents()
        url = f'{self.host}/user-session'
        response = self.obj.create_api(url, headers, data)
        auth_token = self.get_authtoken(response)
        return auth_token
        
  

    def stacks(self, api_key):
        headers = self.user_agents()
        headers['authtoken'] = self.auth_token
        headers['api_key'] = api_key
        url = f'{self.host}/stacks'
        return Stacks(url, headers)



    def get_authtoken(self, result):
        return result["user"]["authtoken"]




    def get_host(self):

        if self.region == 'eu': 
            self.host = 'eu-cdn.contentstack.com'
        elif self.region == 'azure-na': 
            self.host = 'azure-na-cdn.contentstack.com'
        elif self.region == 'azure-eu':
            self.host = 'azure-eu-cdn.contentstack.com'
        elif self.region == 'us':
            self.host =  DEFAULT_HOST
        self.endpoint = f'https://{self.host}/{self.version}'

        return self.endpoint

    def user_agents(self):
        return {'Content-Type': 'application/json'}



