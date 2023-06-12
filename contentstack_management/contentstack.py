import platform

import contentstack_management
from .core.client import ApiClient


default_host = 'api.contentstack.io'
default_endpoint = 'https://api.contentstack.io'
default_api_version = 'v3'
default_protocol = 'https://'
default_timeout = 30
default_max_request = 5


def __platform():
    os_platform = platform.system()
    if os_platform == 'Darwin':
        os_platform = 'macOS'
    elif not os_platform or os_platform == 'Java':
        os_platform = None
    elif os_platform and os_platform not in ['macOS', 'Windows']:
        os_platform = 'Linux'
    os_platform = {'name': os_platform, 'version': platform.release()}
    return os_platform


def user_agents(headers):
    headers.update({'sdk': dict(
        name=contentstack_management.__package__,
        version=contentstack_management.__version__
    ), 'os': str(__platform())})

    package = f"contentstack-management-python/{contentstack_management.__version__}"
    return {'User-Agent': str(headers), "X-User-Agent": package, 'Content-Type': 'application/json' }


def client(endpoint=None,
           host: str = None, authtoken: str = None, headers=None, authorization: str = None,
           timeout: int = None, failure_retry: int = 0, exceptions: bool = True,
           errors: bool = True, max_requests: int = default_max_request, retry_on_error: bool = True):
    """
    :param endpoint: Optional API endpoint.
    :param host: Optional hostname for the API endpoint.
    :param authtoken: Optional authentication token for API requests
    :param headers: Optional headers to be included with API requests
    :param authorization: Optional authorization value for API requests
    :param timeout: Optional timeout value for API requests
    :param failure_retry: Optional number of retries for API requests that fail
    :param exceptions: Optional boolean value indicating whether to handle exceptions during API requests
    :param errors: Optional boolean value indicating whether to handle errors during API requests.
    :param max_requests:Optional maximum number of requests to be made
    :param retry_on_error: Optional boolean value indicating whether to retry API requests on error.
    :return: A client object for performing API operations.
    -------------------------------
    [Example:]
    
        >>> from contentstack_management import contentstack
        >>> client = contentstack.client()
    -------------------------------
    """
    if headers is None:
        headers = {}
    headers = user_agents(headers)
    if host is None:
        host = contentstack_management.__host__

    if endpoint is None:
        endpoint = contentstack_management.__endpoint__
        if host is not None:
            endpoint = f'{contentstack_management.__protocol__}{host}/{contentstack_management.__api_version__}'

    if timeout is None:
        timeout = default_timeout

    return ApiClient(host=host, endpoint=endpoint, authtoken=authtoken,
                     headers=headers, authorization=authorization,
                     timeout=timeout, failure_retry=failure_retry, exceptions=exceptions, errors=errors,
                     max_requests=max_requests, retry_on_error=retry_on_error)

