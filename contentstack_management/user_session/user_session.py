import platform
import http.cookiejar
import urllib.request
import contentstack_management


class UserSession:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, url = None, headers=None, data=None, api_client=None, endpoint=None):
        self.data = data
        self.url = url
        self.headers = headers
        self.api_client = api_client
        self.endpoint= endpoint
        

    
    def login(self):
        response =  self.api_client._call_request('POST', self.url, headers=self.headers, params=None, data=self.data, json_data=None)
        if response.status_code == 200:
            response_dict = response.json()
            token = response_dict['user']['authtoken']
            if token:
               # Create a CookieJar
                cookie_jar = http.cookiejar.CookieJar()
                # Set a cookie
                cookie =  cookie_jar.set_cookie(http.cookiejar.Cookie(
                    version=0,
                    name='auth_token',
                    value=token,
                    port=None,
                    port_specified=False,
                    domain=self.endpoint,
                    domain_specified=True,
                    domain_initial_dot=False,
                    path='/',
                    path_specified=True,
                    secure=False,
                    expires=None,
                    discard=False,
                    comment=None,
                    comment_url=None,
                    rest=None,
                    rfc2109=False,
                ))
                return response

        return response
    
    def logout(self):
       
        response =  self.api_client._call_request('DELETE', self.url, headers=self.headers, params=None, data=self.data, json_data=None)
        if response.status_code == 200:
            return response.json()
        return response

