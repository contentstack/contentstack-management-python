import requests


class _APIClient:
    def __init__(self, endpoint, headers, timeout=30, max_retries: int = 5):
        """
        The function is a constructor that initializes the endpoint, headers, timeout, and max_retries
        attributes of an object.
        
        :param endpoint: The `endpoint` parameter is the URL or address of the API endpoint that you
        want to connect to. It is the destination where you will send your requests and receive
        responses from
        :param headers: The `headers` parameter is used to pass any additional headers that need to be
        included in the HTTP request. Headers are used to provide additional information about the
        request, such as authentication credentials or content type
        :param timeout: The `timeout` parameter specifies the maximum amount of time (in seconds) that
        the request should wait for a response before timing out, defaults to 30 (optional)
        :param max_retries: The `max_retries` parameter is an integer that specifies the maximum number
        of times a request should be retried if it fails. If a request fails, the code will attempt to
        retry the request up to `max_retries` times before giving up, defaults to 5
        :type max_retries: int (optional)
        """
        
        self.endpoint = endpoint
        self.headers = headers
        self.timeout = timeout
        self.max_retries = max_retries
        pass

    def _call_request(self, method, url, headers: dict = None, params=None, data=None, json_data=None, files=None):
        """
        The function `_call_request` sends an HTTP request using the specified method, URL, headers,
        parameters, data, and JSON data, and returns the response as a JSON object.
        
        :param method: The HTTP method to be used for the request (e.g., GET, POST, PUT, DELETE, etc.)
        :param url: The `url` parameter is a string that represents the URL of the API endpoint that you
        want to make a request to
        :param headers: The `headers` parameter is a dictionary that contains the HTTP headers to be
        included in the request. These headers provide additional information about the request, such as
        the content type or authentication credentials
        :type headers: dict
        :param params: The `params` parameter is used to pass query parameters in the URL. These
        parameters are used to filter or modify the response from the server. For example, if you are
        making a request to an API that returns a list of users, you can use the `params` parameter to
        specify the number
        :param data: The `data` parameter is used to send data in the body of the request. It is
        typically used for sending form data or other types of data that are not in JSON format
        :param json_data: The `json_data` parameter is used to send a JSON payload in the request. It is
        typically used when making a POST or PUT request to send data to the server in JSON format. The
        `json_data` parameter should be a dictionary that will be converted to JSON before sending the
        request
        :return: the JSON response from the HTTP request.
        """
        
        # headers.update(self.headers)
        response = requests.request(
            method, url, headers=headers, params=params, data=data, json=json_data, files=files)
        # response.raise_for_status()
        return response

    def get(self, path, params=None, headers=None):
        """
        The function sends a GET request to a specified URL with optional parameters and headers.
        
        :param path: The path parameter is a string that represents the endpoint or path of the API that
        you want to make a GET request to. For example, if you want to make a GET request to the
        "/users" endpoint, you would pass "/users" as the path parameter
        :param params: The `params` parameter is used to pass query parameters in the URL. These
        parameters are used to filter or modify the data being requested from the server. For example,
        if you want to retrieve only the data for a specific user, you can pass the user ID as a query
        parameter
        :param headers: The `headers` parameter is a dictionary that contains any additional headers
        that you want to include in the HTTP request. These headers can be used to provide additional
        information to the server, such as authentication credentials or content type. If no headers are
        provided, the `headers` parameter will default to `None
        :return: The method is returning the result of the `_call_request` method.
        """

        url = f"{self.endpoint}{path}"
        # self.headers = headers or {}
        return self._call_request('GET', url, headers=headers, params=params)

    def put(self, path, data=None, params=None, json_data=None, headers=None, files=None):
        """
        The function sends a PUT request to a specified URL with optional data, parameters, JSON data,
        and headers.
        
        :param path: The path parameter is the endpoint or URL path where the PUT request will be sent
        to. It specifies the location of the resource that needs to be updated or modified
        :param data: The `data` parameter is used to pass the request body data in the form of a string.
        It is typically used for sending data in formats like JSON or XML
        :param params: The `params` parameter is used to pass query parameters in the URL. These
        parameters are used to filter or modify the data being requested from the server
        :param json_data: The `json_data` parameter is used to pass JSON data in the request body. It is
        typically used when making a PUT request to update or modify a resource on the server. The JSON
        data should be a dictionary or a JSON serializable object
        :param headers: The `headers` parameter is used to specify any additional headers that should be
        included in the HTTP request. Headers are used to provide additional information about the
        request, such as the content type or authentication credentials
        :return: the result of calling the `_call_request` method with the specified parameters.
        """
        
        url = f"{self.endpoint}{path}"
        # headers = headers or {}
        return self._call_request('PUT', url, headers=headers, params=params, data=data, json_data=json_data, files=files)

    def post(self, path, data=None, json_data=None, headers=None, params=None, files=None):
        """
        The function sends a POST request to a specified URL with optional data, headers, and
        parameters.
        
        :param path: The path parameter is the endpoint or URL path where the POST request will be sent
        to. It is appended to the base URL or endpoint of the API
        :param data: The `data` parameter is used to pass data in the request body. It can be a
        dictionary, bytes, or a file-like object. This parameter is typically used for sending form data
        or other types of data that are not in JSON format
        :param json_data: The `json_data` parameter is used to pass JSON data in the request body. It is
        typically used when sending data to an API that expects JSON data
        :param headers: The `headers` parameter is used to specify any additional headers that should be
        included in the HTTP request. Headers are used to provide additional information about the
        request, such as the content type or authentication credentials
        :param params: The `params` parameter is used to pass query parameters in the URL. Query
        parameters are used to filter or sort the data being requested from the server. They are
        appended to the URL after a question mark (?) and separated by ampersands (&). For example, if
        you have a `params`
        :return: The method is returning the result of the `_call_request` method.
        """
        
        url = f"{self.endpoint}{path}"
        # headers = headers or {}
        return self._call_request('POST', url, headers=headers, params=params, data=data, json_data=json_data, files=files)

    def delete(self, path, headers=None, params=None, data=None):
        """
        The function sends a DELETE request to a specified URL with optional headers and parameters.
        
        :param path: The `path` parameter is a string that represents the path of the resource you want
        to delete. It is appended to the base URL to form the complete URL for the DELETE request
        :param headers: The `headers` parameter is a dictionary that contains any additional headers
        that you want to include in the DELETE request. These headers can be used to provide additional
        information or authentication credentials to the server. If no headers are provided, the value
        of `headers` will be set to `None`
        :param params: The `params` parameter is used to pass query parameters in the URL. Query
        parameters are used to filter or modify the data being requested. They are appended to the URL
        after a question mark (?) and separated by ampersands (&). For example, if you want to filter
        the data by a specific
        :return: The method is returning the result of the `_call_request` method, which is the response
        from the DELETE request made to the specified URL.
        """
        
        url = f"{self.endpoint}{path}"
        # headers = headers or {}
        return self._call_request('DELETE', url, headers=headers, params=params, data = data)
