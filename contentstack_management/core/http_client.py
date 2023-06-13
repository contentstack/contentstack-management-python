"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import requests
import json


class HttpClient:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, endpoint):
        #init method
        self.url="user"
        self.endpoint = endpoint
        self.failure_retry = 0
        self.exceptions = True
        self.errors = True



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
                    return response.json()

            except Exception as e:
                if self.exceptions:
                    raise e
                elif retries > 1:
                    retries -= 1
                else:
                    return None
                
    
