"""
OAuth Interceptor for automatic token management and request handling.
"""

import time
import threading
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OAuthInterceptor:
    """
    OAuth interceptor that automatically handles token refresh and request retries.
    """
    MAX_RETRIES = 3
    REFRESH_TIMEOUT = 30 
    TOKEN_ENDPOINT_PATH = "/token"
    TOKEN_REFRESH_FAILED_MSG = "Token refresh failed"
    NO_VALID_TOKENS_MSG = "OAuth: No valid tokens available"
    TOKEN_REFRESH_FAILED_AFTER_401_MSG = "OAuth: Token refresh failed after 401"
    # User agent strings
    USER_AGENT = "contentstack-python-management-sdk"
    X_USER_AGENT = "contentstack-python-management-sdk"
    
    def __init__(self, oauth_handler):
        """
        Initialize the OAuth interceptor.
        Args:
            oauth_handler: The OAuthHandler instance
        """
        self.oauth_handler = oauth_handler
        self.early_access = None
        self.refresh_lock = threading.Lock()
    
    def set_early_access(self, early_access: list):
        """Set early access headers."""
        self.early_access = early_access
    
    def is_oauth_configured(self) -> bool:
        """Check if OAuth is properly configured."""
        return (self.oauth_handler is not None and 
                hasattr(self.oauth_handler, 'app_id') and 
                self.oauth_handler.app_id is not None)
    
    def has_valid_tokens(self) -> bool:
        """Check if we have valid (non-expired) tokens."""
        if not self.oauth_handler or not hasattr(self.oauth_handler, 'api_client'):
            return False
        
        api_client = self.oauth_handler.api_client
        if not hasattr(api_client, 'oauth') or not api_client.oauth:
            return False
        return not self.oauth_handler.is_token_expired()
    
    def _get_default_headers(self, request_url: str) -> Dict[str, str]:
        """
        Get default headers for requests.
        Returns:
            Dictionary of headers
        """
        headers = {
            "X-User-Agent": self.X_USER_AGENT,
            "User-Agent": self.USER_AGENT,
            "x-header-ea": ",".join(self.early_access) if self.early_access else "true"
        }
        
        if self.TOKEN_ENDPOINT_PATH in request_url:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            headers["Content-Type"] = "application/json"
        
        return headers
    
    def _add_auth_header(self, headers: Dict[str, str], request_url: str) -> Dict[str, str]:
        """
        Add authorization header if appropriate.
        Returns:
            Updated headers with authorization if needed
        """
        if self.TOKEN_ENDPOINT_PATH in request_url:
            return headers
        if (self.oauth_handler and 
            hasattr(self.oauth_handler, 'api_client') and
            self.oauth_handler.api_client and
            hasattr(self.oauth_handler.api_client, 'oauth') and
            self.oauth_handler.api_client.oauth and
            self.oauth_handler.api_client.oauth.get('accessToken')):
            
            headers["Authorization"] = f"Bearer {self.oauth_handler.api_client.oauth['accessToken']}"
        return headers
    
    def _ensure_valid_token(self) -> bool:
        """
        Ensure we have a valid token, refreshing if necessary.
        Returns:
            True if we have a valid token, False otherwise
        """
        if not self.oauth_handler or not hasattr(self.oauth_handler, 'api_client'):
            return False
        
        api_client = self.oauth_handler.api_client
        if not hasattr(api_client, 'oauth') or not api_client.oauth:
            return False
        
        # Check if token is expired and refresh if needed
        if self.oauth_handler.is_token_expired():
            with self.refresh_lock:
                try:
                    if self.oauth_handler.is_token_expired():
                        self.oauth_handler.refresh_access_token()
                    return True
                except Exception as e:
                    print(f"{self.TOKEN_REFRESH_FAILED_MSG}: {e}")
                    return False
        
        return True
    
    def execute_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Execute a request with OAuth handling and retry logic.
        Returns:
            Response object
        """
        if self.TOKEN_ENDPOINT_PATH in url:
            return self._make_request(method, url, **kwargs)
        if not self._ensure_valid_token():
            raise requests.RequestException(self.NO_VALID_TOKENS_MSG)
        return self._execute_with_retry(method, url, 0, **kwargs)
    
    def _execute_with_retry(self, method: str, url: str, retry_count: int, **kwargs) -> requests.Response:
        """
        Execute request with retry logic.
        Returns:
            Response object
        """
        headers = self._get_default_headers(url)
        headers = self._add_auth_header(headers, url)
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        response = self._make_request(method, url, **kwargs)
        if not response.ok and retry_count < self.MAX_RETRIES:
            status_code = response.status_code
            
            if (status_code == 401 and 
                self.oauth_handler and 
                hasattr(self.oauth_handler, 'api_client') and
                self.oauth_handler.api_client and
                hasattr(self.oauth_handler.api_client, 'oauth') and
                self.oauth_handler.api_client.oauth and
                self.oauth_handler.api_client.oauth.get('refreshToken')):
                
                with self.refresh_lock:
                    try:
                        self.oauth_handler.refresh_access_token()
                        headers["Authorization"] = f"Bearer {self.oauth_handler.api_client.oauth['accessToken']}"
                        kwargs['headers'] = headers
                        return self._execute_with_retry(method, url, retry_count + 1, **kwargs)
                    except Exception as e:
                        raise requests.RequestException(f"{self.TOKEN_REFRESH_FAILED_AFTER_401_MSG}: {e}")
            
            if status_code == 429 or (status_code >= 500 and status_code != 501):
                # Calculate delay with exponential backoff
                delay = min(1000 * (2 ** retry_count), 30000) / 1000  # Convert to seconds
                time.sleep(delay)
                return self._execute_with_retry(method, url, retry_count + 1, **kwargs)
        return response
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make the actual HTTP request.
        Returns:
            Response object
        """
        return requests.request(method, url, **kwargs)
    
    def get_valid_access_token(self) -> Optional[str]:
        """
        Get a valid access token, refreshing if necessary.
        Returns:
            Valid access token or None if unavailable
        """
        if self._ensure_valid_token():
            return self.oauth_handler.api_client.oauth.get('accessToken')
        return None
