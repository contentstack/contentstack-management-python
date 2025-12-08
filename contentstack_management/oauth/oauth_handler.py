"""
OAuth 2.0 Handler for Contentstack Management SDK.

This module provides OAuth 2.0 authentication support including:
- Authorization code flow
- PKCE (Proof Key for Code Exchange)
- Token management and refresh
- Secure token storage
"""

import hashlib
import secrets
import time
import urllib.parse
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse, parse_qs

import requests
from .._messages import (
    OAUTH_ACCESS_TOKEN_EXPIRED,
    OAUTH_ACCESS_TOKEN_NOT_AVAILABLE,
    OAUTH_TOKENS_NOT_AVAILABLE,
    OAUTH_REFRESH_TOKEN_NOT_AVAILABLE,
    OAUTH_NOT_CONFIGURED,
    OAUTH_AUTHORIZATION_CODE_NOT_FOUND,
    OAUTH_TOKEN_EXCHANGE_FAILED,
    OAUTH_TOKEN_REFRESH_FAILED,
    OAUTH_BASE_URL_NOT_SET,
    OAUTH_AUTHORIZING,
    OAUTH_AUTHORIZATION_URL_GENERATED,
    OAUTH_AUTHORIZATION_URL_GENERATION_FAILED,
    OAUTH_AUTHORIZATION_CODE_EMPTY,
    OAUTH_TOKEN_EXCHANGE_ERROR,
    OAUTH_TOKEN_REFRESH_ERROR
)


class OAuthHandler:
    """
    OAuth 2.0 Handler for Contentstack Management SDK.
    
    This class manages OAuth 2.0 authentication flow including authorization,
    token exchange, refresh, and secure storage.
    """
    
    # Base URLs
    OAUTH_BASE_URL = 'https://app.contentstack.com'
    DEVELOPER_HUB_BASE_URL = 'https://developerhub-api.contentstack.com'
    
    def __init__(
        self,
        app_id: str,
        client_id: str,
        redirect_uri: str,
        response_type: str = "code",
        client_secret: Optional[str] = None,
        scope: Optional[List[str]] = None,
        api_client=None
    ):
        self.app_id = app_id
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = ' '.join(scope) if scope else ''
        self.client_secret = client_secret  # Optional, if provided, PKCE will be skipped
        self.api_client = api_client
        
        self._oauth_base_url = self._construct_oauth_base_url()
        self._developer_hub_base_url = self._construct_developer_hub_base_url()
        
        if self.api_client:
            if not hasattr(self.api_client, 'oauth'):
                self.api_client.oauth = {}
            self.api_client.oauth.update({
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'app_id': app_id
            })
        
        # PKCE setup
        self.use_pkce = client_secret is None
        if self.use_pkce:
            self.code_verifier = self._generate_code_verifier()
            self.code_challenge = self._generate_code_challenge(self.code_verifier)
        else:
            self.code_verifier = None
            self.code_challenge = None
    
    def _construct_oauth_base_url(self) -> str:
        """
        Construct OAuth base URL based on api_client endpoint using dynamic text replacement.
        Returns:
            OAuth base URL string
        """
        if not self.api_client or not hasattr(self.api_client, 'endpoint'):
            return self.OAUTH_BASE_URL
        
        endpoint = self.api_client.endpoint
        
        from urllib.parse import urlparse
        parsed = urlparse(endpoint)
        domain = parsed.netloc
        if 'api.contentstack.io' in domain:
            oauth_domain = domain.replace('api.contentstack.io', 'app.contentstack.com')
        else:
            oauth_domain = domain.replace('-api.', '-app.').replace('api.', 'app.')
        oauth_url = f'https://{oauth_domain}'
        return oauth_url
    
    def _construct_developer_hub_base_url(self) -> str:
        """
        Construct Developer Hub base URL based on api_client endpoint using dynamic text replacement.
        Returns:
            Developer Hub base URL string
        """
        if not self.api_client or not hasattr(self.api_client, 'endpoint'):
            return self.DEVELOPER_HUB_BASE_URL
        
        endpoint = self.api_client.endpoint
        from urllib.parse import urlparse
        parsed = urlparse(endpoint)
        domain = parsed.netloc
        
        if 'api.contentstack.io' in domain:
            dev_hub_domain = domain.replace('api.contentstack.io', 'developerhub-api.contentstack.com')
        else:
            dev_hub_domain = domain.replace('-api.', '-developerhub-api.')
        dev_hub_url = f'https://{dev_hub_domain}'
        return dev_hub_url
    
    def _generate_code_verifier(self, length: int = 128) -> str:
        """
        Generate a random code verifier for PKCE.
        Returns:
            Base64 URL-encoded code verifier
        """
        code_verifier = secrets.token_urlsafe(length)
        return code_verifier
    
    def _generate_code_challenge(self, code_verifier: str) -> str:
        """
        Generate code challenge from code verifier using SHA256.
        Returns:
            Base64 URL-encoded SHA256 hash of the code verifier
        """
        sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        import base64
        code_challenge = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
        return code_challenge
    
    def _get_headers(self) -> Dict[str, str]:
        """Get common headers for OAuth requests."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        if (self.api_client and hasattr(self.api_client, 'oauth') and 
            self.api_client.oauth.get('accessToken')):
            headers["authorization"] = f"Bearer {self.api_client.oauth['accessToken']}"
        return headers
    
    def authorize(self) -> str:
        """
        Start the OAuth authorization flow.
        Returns:
            Authorization URL for user to visit
        """
        try:
            print(OAUTH_AUTHORIZING.format(app_id=self.app_id, client_id=self.client_id))  # Debug
            if not self._oauth_base_url:
                raise ValueError(OAUTH_BASE_URL_NOT_SET)
            oauth_base = self._oauth_base_url.rstrip('/')
            base_url = f"{oauth_base}/#!/apps/{self.app_id}/authorize"
            params = {
                'response_type': 'code',  # Always use 'code'
                'client_id': self.client_id
            }
            
            if self.redirect_uri and self.redirect_uri.strip() and self.redirect_uri != 'None':
                params['redirect_uri'] = self.redirect_uri
            
            # Add PKCE parameters if using PKCE
            if self.use_pkce:
                if not self.code_challenge:
                    self.code_challenge = self._generate_code_challenge(self.code_verifier)
                params['code_challenge'] = self.code_challenge
                params['code_challenge_method'] = 'S256'
            
            query_string = urllib.parse.urlencode(params)
            final_url = f"{base_url}?{query_string}"
            print(OAUTH_AUTHORIZATION_URL_GENERATED.format(final_url=final_url))  # Debug
            return final_url
            
        except Exception as e:
            raise ValueError(OAUTH_AUTHORIZATION_URL_GENERATION_FAILED.format(error=e))
    
    def handle_redirect(self, redirect_url: str) -> Dict:
        """
        Handle the redirect from OAuth authorization server.
        Returns:
            Dictionary containing token information
        """
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        if "code" not in query_params:
            raise ValueError(OAUTH_AUTHORIZATION_CODE_NOT_FOUND)
        authorization_code = query_params["code"][0]
        return self.exchange_code_for_token(authorization_code)
    
    def exchange_code_for_token(self, authorization_code: str) -> Dict:
        """
        Exchange authorization code for access token.
        Returns:
            Dictionary containing token information
        """
        if not authorization_code or not authorization_code.strip():
            raise ValueError(OAUTH_AUTHORIZATION_CODE_EMPTY)
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code.strip(),
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "app_id": self.app_id
        }
        
        if self.client_secret:
            data["client_secret"] = self.client_secret
        else:
            data["code_verifier"] = self.code_verifier
        
        headers = self._get_headers()
        
        try:
            token_endpoint = f"{self._developer_hub_base_url}/token"
            response = requests.post(
                token_endpoint,
                data=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()
            self._save_tokens(token_data)
            return token_data
            
        except requests.RequestException as e:
            raise requests.RequestException(OAUTH_TOKEN_EXCHANGE_ERROR.format(error=str(e)))
    
    def _save_tokens(self, token_data: Dict):
        """
        Save tokens and related information.
        """
        # Store tokens in api_client.oauth
        if self.api_client:
            self.api_client.oauth["accessToken"] = token_data.get("access_token")
            self.api_client.oauth["refreshToken"] = token_data.get("refresh_token") or self.api_client.oauth.get("refreshToken")
            self.api_client.oauth["organizationUID"] = token_data.get("organization_uid")
            self.api_client.oauth["userUID"] = token_data.get("user_uid")
            expires_in = token_data.get("expires_in", 3600)
            self.api_client.oauth["tokenExpiryTime"] = int(time.time() * 1000) + (expires_in - 60) * 1000  # Store expiry time in milliseconds
        
        self._access_token = token_data.get("access_token")
        self._refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
        self._token_expiry_time = time.time() + expires_in
        self._organization_uid = token_data.get("organization_uid")
        self._user_uid = token_data.get("user_uid")
        if self.api_client and self._access_token:
            self.api_client.headers["Authorization"] = f"Bearer {self._access_token}"
    
    def get_valid_access_token(self) -> str:
        """
        Get valid access token, refreshing if necessary.
        Returns:
            Valid access token
        """
        if self.is_token_expired():
            print(OAUTH_ACCESS_TOKEN_EXPIRED)
            self.refresh_access_token()
        access_token = self.get_access_token()
        if not access_token:
            raise ValueError(OAUTH_ACCESS_TOKEN_NOT_AVAILABLE)
        return access_token
    
    def is_token_expired(self) -> bool:
        """
        Check if access token is expired.
        Returns:
            True if token is expired, False otherwise
        """
        if not self.api_client or not hasattr(self.api_client, 'oauth'):
            return True
        
        token_expiry_time = self.api_client.oauth.get('tokenExpiryTime')
        if not token_expiry_time:
            return True
        if token_expiry_time > 1e10:
            expiry_time = token_expiry_time / 1000
        else:
            expiry_time = token_expiry_time
        return time.time() >= expiry_time
    
    def refresh_access_token(self) -> str:
        """
        Refresh the access token using refresh token.
        Returns:
            New access token
        """
        if not self.api_client or not hasattr(self.api_client, 'oauth') or not self.api_client.oauth:
            raise ValueError(OAUTH_TOKENS_NOT_AVAILABLE)
        refresh_token = self.api_client.oauth.get('refreshToken')
        if not refresh_token:
            raise ValueError(OAUTH_REFRESH_TOKEN_NOT_AVAILABLE)
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "app_id": self.app_id
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret
        headers = self._get_headers()
        try:
            response = requests.post(
                f"{self._developer_hub_base_url}/token",
                data=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self._save_tokens(token_data)
            
            return self._access_token
        except requests.RequestException as e:
            raise requests.RequestException(OAUTH_TOKEN_REFRESH_ERROR.format(error=str(e)))
    
    def logout(self, revoke_authorization: bool = True) -> bool:
        """
        Logout and clear OAuth tokens.
        Returns:
            True if logout successful, False otherwise
        """
        try:
            self._clear_tokens()
            return True
            
        except Exception:
            self._clear_tokens()
            return False
    
    def _clear_tokens(self):
        """Clear all stored tokens and related information."""
        self._access_token = None
        self._refresh_token = None
        self._token_expiry_time = None
        self._organization_uid = None
        self._user_uid = None
        
        if self.api_client and "Authorization" in self.api_client.headers:
            del self.api_client.headers["Authorization"]
    
    def get_access_token(self) -> Optional[str]:
        """Get the current access token."""
        return self._access_token
    
    def set_access_token(self, token: str):
        """Set the access token."""
        self._access_token = token
        if self.api_client:
            self.api_client.headers["Authorization"] = f"Bearer {token}"
            if not hasattr(self.api_client, 'oauth'):
                self.api_client.oauth = {}
            self.api_client.oauth['accessToken'] = token
    
    def get_refresh_token(self) -> Optional[str]:
        """Get the current refresh token."""
        return self._refresh_token
    
    def set_refresh_token(self, token: str):
        """Set the refresh token."""
        self._refresh_token = token
        if self.api_client:
            if not hasattr(self.api_client, 'oauth'):
                self.api_client.oauth = {}
            self.api_client.oauth['refreshToken'] = token
    
    def get_organization_uid(self) -> Optional[str]:
        """Get the organization UID."""
        return self._organization_uid
    
    def set_organization_uid(self, uid: str):
        """Set the organization UID."""
        self._organization_uid = uid
    
    def get_user_uid(self) -> Optional[str]:
        """Get the user UID."""
        return self._user_uid
    
    def set_user_uid(self, uid: str):
        """Set the user UID."""
        self._user_uid = uid
    
    def get_token_expiry_time(self) -> Optional[float]:
        """Get the token expiry time."""
        return self._token_expiry_time
    
    def set_token_expiry_time(self, expiry_time: float):
        """Set the token expiry time."""
        self._token_expiry_time = expiry_time
        if self.api_client:
            if not hasattr(self.api_client, 'oauth'):
                self.api_client.oauth = {}
            self.api_client.oauth['tokenExpiryTime'] = expiry_time
    
