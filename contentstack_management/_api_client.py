import requests


class _APIClient:
    def __init__(self, endpoint, headers, timeout=30, max_retries: int = 5):
        self.endpoint = endpoint
        self.headers = headers
        self.timeout = timeout
        self.max_retries = max_retries
        pass

    def _call_request(self, method, url, headers: {} = None, params=None, data=None, json_data=None):
        headers.update(self.headers)
        response = requests.request(
            method, url, headers=headers, params=params, data=data, json=json_data)
        response.raise_for_status()
        return response.json()

    def get(self, path, params=None, headers=None):
        url = f"{self.endpoint}{path}"
        self.headers = headers or {}
        return self._call_request('GET', url, headers=headers, params=params)

    def put(self, path, data=None, params=None, json_data=None, headers=None):
        url = f"{self.endpoint}{path}"
        headers = headers or {}
        return self._call_request('PUT', url, headers=headers, params=params, data=data, json_data=json_data)

    def post(self, path, data=None, json_data=None, headers=None, params=None):
        url = f"{self.endpoint}{path}"
        headers = headers or {}
        return self._call_request('POST', url, headers=headers, params=params, data=data, json_data=json_data)

    def delete(self, path, headers=None, params=None):
        url = f"{self.endpoint}{path}"
        headers = headers or {}
        return self._call_request('DELETE', url, headers=headers, params=params)
