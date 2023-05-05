"""This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API """

import json
from json import JSONDecodeError
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
import contentstack_cms


TIMEOUT=30
RETRY_STRATEGY='Retry(total=5, backoff_factor=0, status_forcelist=[408, 429])'


class HttpClient:
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self):
        self.retry_strategy = RETRY_STRATEGY
        self.timeout = TIMEOUT


    def create_api(self, url, headers, body):
        try:
            data = json.dumps(body)
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            response = session.post(url, verify=True, headers=headers, timeout=self.timeout, data=data)
            session.close()
            if response.encoding is None:
                response.encoding = 'utf-8'
            elif response is not None:
                return response.json()
            else:
                return {"error": "error details not found", "error_code": 422,
                        "error_message": "unknown error"}
        except Timeout as timeout_err:
            raise TimeoutError(
                json.dumps({"httpStatus": 408,
                            "message": f'Timeout error ${timeout_err.strerror}'})) from timeout_err
        except ConnectionError as connect_err:
            raise ConnectionError(json.dumps({"httpStatus": 503,
                                              "message": f'Service error ${connect_err.strerror}'})) from connect_err
        except JSONDecodeError as connection_err:
            raise TypeError(json.dumps({"httpStatus": 503,
                                        "message": 'Decoding JSON has failed.'})) from connection_err
        except HTTPError as http_err:
            raise HTTPError('Http error occurred') from http_err

            

    def read_api(self, url, headers, unique_id=None):
        """The read() method takes an optional id argument, which specifies 
        the id of the resource to read. If no ID is provided, it returns a 
        list of all resources at the base URL. If an ID is provided, 
        it returns the JSON for that specific resource"""
        try:
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            response = session.get(url, verify=True, headers=headers, timeout=self.timeout)
            session.close()
            if response.encoding is None:
                response.encoding = 'utf-8'
            elif response is not None:
                return response.json()
            else:
                return {"error": "error details not found", "error_code": 422,
                        "error_message": "unknown error"}
        except Timeout as timeout_err:
            raise TimeoutError(
                json.dumps({"httpStatus": 408,
                            "message": f'Timeout error ${timeout_err.strerror}'})) from timeout_err
        except ConnectionError as connect_err:
            raise ConnectionError(json.dumps({"httpStatus": 503,
                                              "message": f'Service error ${connect_err.strerror}'})) from connect_err
        except JSONDecodeError as connection_err:
            raise TypeError(json.dumps({"httpStatus": 503,
                                        "message": 'Decoding JSON has failed.'})) from connection_err
        except HTTPError as http_err:
            raise HTTPError('Http error occurred') from http_err


    def update_api(self, url, headers, body):
        """To update() method takes an id and a data object as arguments,
        sends a PUT request to the base URL with the updated data in JSON format,
        and returns the response JSON"""
        try:
            data = json.dumps(body)
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            response = session.put(url, verify=True, headers=headers, timeout=self.timeout, data=data)
            session.close()
            if response.encoding is None:
                response.encoding = 'utf-8'
            elif response is not None:
                return response.json()
            else:
                return {"error": "error details not found", "error_code": 422,
                        "error_message": "unknown error"}
        except Timeout as timeout_err:
            raise TimeoutError(
                json.dumps({"httpStatus": 408,
                            "message": f'Timeout error ${timeout_err.strerror}'})) from timeout_err
        except ConnectionError as connect_err:
            raise ConnectionError(json.dumps({"httpStatus": 503,
                                              "message": f'Service error ${connect_err.strerror}'})) from connect_err
        except JSONDecodeError as connection_err:
            raise TypeError(json.dumps({"httpStatus": 503,
                                        "message": 'Decoding JSON has failed.'})) from connection_err
        except HTTPError as http_err:
            raise HTTPError('Http error occurred') from http_err


    def delete_api(self, url, headers):
        """To delete() method takes an id as an argument,
        sends a DELETE request to the base URL with the id, 
        and returns the response JSON"""
        try:
            self.headers = user_agents()
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            response = session.delete(url, verify=True, headers=headers, timeout=self.timeout)
            session.close()
            if response.encoding is None:
                response.encoding = 'utf-8'
            elif response is not None:
                return response.json()
            else:
                return {"error": "error details not found", "error_code": 422,
                        "error_message": "unknown error"}
        except Timeout as timeout_err:
            raise TimeoutError(
                json.dumps({"httpStatus": 408,
                            "message": f'Timeout error ${timeout_err.strerror}'})) from timeout_err
        except ConnectionError as connect_err:
            raise ConnectionError(json.dumps({"httpStatus": 503,
                                              "message": f'Service error ${connect_err.strerror}'})) from connect_err
        except JSONDecodeError as connection_err:
            raise TypeError(json.dumps({"httpStatus": 503,
                                        "message": 'Decoding JSON has failed.'})) from connection_err
        except HTTPError as http_err:
            raise HTTPError('Http error occurred') from http_err


 







