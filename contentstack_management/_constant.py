import platform
import sys 


def _default_user_agent():
    """
    The function `_default_user_agent()` returns a dictionary containing information about the user
    agent, including the SDK, app, platform, and operating system.
    :return: a dictionary containing information about the user agent.
    """

    header = {
        'sdk': {
            'name': 'contentstack-management.python',
            'version': sys.version_info
        },
        'app': {
            'name': 'contentstack-management.python',
            'version': '1.0.0'
        },
        'platform': {
            'name': 'python',
            'version': platform.python_version()
        }
    }

    os_name = platform.system()
    if os_name == 'Darwin':
        os_name = 'macOS'
    elif not os_name or os_name == 'Java':
        os_name = None
    elif os_name not in ['macOS', 'Windows']:
        os_name = 'Linux'

    header['os'] = {
        'name': os_name,
        'version': platform.release() if os_name else None
    }

    return header


def _request_headers():
    """
    The function `_request_headers` returns a dictionary of headers for an HTTP request.
    :return: a dictionary containing the headers for a HTTP request.
    """
    
    headers = {
        'X-User-Agent': _default_user_agent(),
        'Content-Type':
            'application/json',
    }
    return headers


if __name__ == '__main__':
    print(_request_headers().__str__())
