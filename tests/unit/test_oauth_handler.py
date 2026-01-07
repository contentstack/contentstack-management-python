"""
Unit tests for OAuth Handler functionality.
"""

import json
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
import requests

from contentstack_management.oauth.oauth_handler import OAuthHandler


class TestOAuthHandler(unittest.TestCase):
    """Test cases for OAuthHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app_id = "test-app-id"
        self.client_id = "test-client-id"
        self.redirect_uri = "http://localhost:3000/callback"
        self.client_secret = "test-client-secret"
        self.scope = ["read", "write"]
        self.api_client = Mock()
        self.api_client.headers = {}
        self.api_client.endpoint = "https://api.contentstack.io/v3/"
        self.api_client.oauth = {}
        
        # Create OAuth handler with client secret (standard flow)
        self.oauth_handler_with_secret = OAuthHandler(
            app_id=self.app_id,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            client_secret=self.client_secret,
            scope=self.scope,
            api_client=self.api_client
        )
        
        # Create OAuth handler without client secret (PKCE flow)
        self.oauth_handler_pkce = OAuthHandler(
            app_id=self.app_id,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            api_client=self.api_client
        )
    
    def test_initialization_with_client_secret(self):
        """Test OAuth handler initialization with client secret."""
        self.assertEqual(self.oauth_handler_with_secret.app_id, self.app_id)
        self.assertEqual(self.oauth_handler_with_secret.client_id, self.client_id)
        self.assertEqual(self.oauth_handler_with_secret.redirect_uri, self.redirect_uri)
        self.assertEqual(self.oauth_handler_with_secret.client_secret, self.client_secret)
        self.assertEqual(self.oauth_handler_with_secret.scope, 'read write')  # Converted to string
        self.assertFalse(self.oauth_handler_with_secret.use_pkce)
        self.assertIsNone(self.oauth_handler_with_secret.code_verifier)
        self.assertIsNone(self.oauth_handler_with_secret.code_challenge)
    
    def test_initialization_without_client_secret(self):
        """Test OAuth handler initialization without client secret (PKCE)."""
        self.assertEqual(self.oauth_handler_pkce.app_id, self.app_id)
        self.assertEqual(self.oauth_handler_pkce.client_id, self.client_id)
        self.assertEqual(self.oauth_handler_pkce.redirect_uri, self.redirect_uri)
        self.assertIsNone(self.oauth_handler_pkce.client_secret)
        self.assertEqual(self.oauth_handler_pkce.scope, 'read write')  # Converted to string
        self.assertTrue(self.oauth_handler_pkce.use_pkce)
        self.assertIsNotNone(self.oauth_handler_pkce.code_verifier)
        self.assertIsNotNone(self.oauth_handler_pkce.code_challenge)
    
    def test_generate_code_verifier(self):
        """Test code verifier generation."""
        verifier = self.oauth_handler_pkce._generate_code_verifier()
        self.assertIsInstance(verifier, str)
        self.assertGreater(len(verifier), 0)
        
        # Test with custom length (secrets.token_urlsafe returns base64 encoded string)
        verifier_short = self.oauth_handler_pkce._generate_code_verifier(32)
        # Base64 encoding of 32 bytes results in ~43 characters
        self.assertGreaterEqual(len(verifier_short), 32)
    
    def test_generate_code_challenge(self):
        """Test code challenge generation."""
        verifier = "test-code-verifier"
        challenge = self.oauth_handler_pkce._generate_code_challenge(verifier)
        self.assertIsInstance(challenge, str)
        self.assertGreater(len(challenge), 0)
    
    def test_get_headers(self):
        """Test header generation."""
        headers = self.oauth_handler_with_secret._get_headers()
        expected_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        self.assertEqual(headers, expected_headers)
    
    def test_authorize_with_client_secret(self):
        """Test authorization URL generation with client secret."""
        auth_url = self.oauth_handler_with_secret.authorize()
        
        self.assertIn(self.app_id, auth_url)
        self.assertIn(self.client_id, auth_url)
        self.assertIn("http%3A%2F%2Flocalhost%3A3000%2Fcallback", auth_url)  # URL encoded
        self.assertIn("response_type=code", auth_url)
        # Note: scope is not included in the authorization URL as per Contentstack OAuth implementation
        self.assertNotIn("code_challenge", auth_url)
    
    def test_authorize_with_pkce(self):
        """Test authorization URL generation with PKCE."""
        auth_url = self.oauth_handler_pkce.authorize()
        
        self.assertIn(self.app_id, auth_url)
        self.assertIn(self.client_id, auth_url)
        self.assertIn("http%3A%2F%2Flocalhost%3A3000%2Fcallback", auth_url)  # URL encoded
        self.assertIn("response_type=code", auth_url)
        # Note: scope is not included in the authorization URL as per Contentstack OAuth implementation
        self.assertIn("code_challenge", auth_url)
        self.assertIn("code_challenge_method=S256", auth_url)
    
    def test_authorize_without_scope(self):
        """Test authorization URL generation without scope."""
        oauth_handler = OAuthHandler(
            app_id=self.app_id,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri
        )
        auth_url = oauth_handler.authorize()
        
        self.assertNotIn("scope=", auth_url)
    
    def test_handle_redirect_success(self):
        """Test successful redirect handling."""
        redirect_url = "http://localhost:3000/callback?code=test-auth-code&state=test-state"
        
        # Mock the token exchange response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600,
            "organization_uid": "test-org-uid",
            "user_uid": "test-user-uid"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            token_data = self.oauth_handler_with_secret.handle_redirect(redirect_url)
            
            self.assertEqual(token_data["access_token"], "test-access-token")
            self.assertEqual(token_data["refresh_token"], "test-refresh-token")
            self.assertEqual(self.oauth_handler_with_secret.get_access_token(), "test-access-token")
            self.assertEqual(self.oauth_handler_with_secret.get_refresh_token(), "test-refresh-token")
            self.assertEqual(self.oauth_handler_with_secret.get_organization_uid(), "test-org-uid")
            self.assertEqual(self.oauth_handler_with_secret.get_user_uid(), "test-user-uid")
    
    def test_handle_redirect_no_code(self):
        """Test redirect handling with no authorization code."""
        redirect_url = "http://localhost:3000/callback?error=access_denied"
        
        with self.assertRaises(ValueError) as context:
            self.oauth_handler_with_secret.handle_redirect(redirect_url)
        
        self.assertIn("Authorization code was not found in the redirect URL", str(context.exception))
    
    def test_exchange_code_for_token_success(self):
        """Test successful code exchange for token."""
        auth_code = "test-auth-code"
        
        # Mock the token exchange response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600,
            "organization_uid": "test-org-uid",
            "user_uid": "test-user-uid"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            token_data = self.oauth_handler_with_secret.exchange_code_for_token(auth_code)
            
            self.assertEqual(token_data["access_token"], "test-access-token")
            self.assertEqual(self.oauth_handler_with_secret.get_access_token(), "test-access-token")
            self.assertEqual(self.oauth_handler_with_secret.get_refresh_token(), "test-refresh-token")
    
    def test_exchange_code_for_token_with_pkce(self):
        """Test code exchange with PKCE flow."""
        auth_code = "test-auth-code"
        
        # Mock the token exchange response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            self.oauth_handler_pkce.exchange_code_for_token(auth_code)
            
            # Verify that code_verifier was included in the request
            call_args = mock_post.call_args
            self.assertIn("code_verifier", call_args[1]["data"])
    
    def test_exchange_code_for_token_failure(self):
        """Test code exchange failure."""
        auth_code = "invalid-auth-code"
        
        # Mock the failed response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException("Token exchange failed")
        
        with patch('requests.post', return_value=mock_response):
            with self.assertRaises(requests.RequestException):
                self.oauth_handler_with_secret.exchange_code_for_token(auth_code)
    
    def test_refresh_access_token_success(self):
        """Test successful access token refresh."""
        # Set up initial tokens
        self.oauth_handler_with_secret.set_refresh_token("test-refresh-token")
        
        # Mock the refresh response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new-access-token",
            "refresh_token": "new-refresh-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            new_token = self.oauth_handler_with_secret.refresh_access_token()
            
            self.assertEqual(new_token, "new-access-token")
            self.assertEqual(self.oauth_handler_with_secret.get_access_token(), "new-access-token")
            self.assertEqual(self.oauth_handler_with_secret.get_refresh_token(), "new-refresh-token")
    
    def test_refresh_access_token_no_refresh_token(self):
        """Test refresh access token without refresh token."""
        with self.assertRaises(ValueError) as context:
            self.oauth_handler_with_secret.refresh_access_token()
        
        self.assertIn("Refresh token is not available", str(context.exception))
    
    def test_refresh_access_token_failure(self):
        """Test refresh access token failure."""
        self.oauth_handler_with_secret.set_refresh_token("invalid-refresh-token")
        
        # Mock the failed response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException("Refresh failed")
        
        with patch('requests.post', return_value=mock_response):
            with self.assertRaises(requests.RequestException):
                self.oauth_handler_with_secret.refresh_access_token()
    
    def test_is_token_expired(self):
        """Test token expiry checking."""
        # No expiry time set
        self.assertTrue(self.oauth_handler_with_secret.is_token_expired())
        
        # Set future expiry time
        future_time = time.time() + 3600
        self.oauth_handler_with_secret.set_token_expiry_time(future_time)
        self.assertFalse(self.oauth_handler_with_secret.is_token_expired())
        
        # Set past expiry time
        past_time = time.time() - 3600
        self.oauth_handler_with_secret.set_token_expiry_time(past_time)
        self.assertTrue(self.oauth_handler_with_secret.is_token_expired())
    
    def test_get_valid_access_token_with_valid_token(self):
        """Test getting valid access token when token is valid."""
        self.oauth_handler_with_secret.set_access_token("valid-token")
        self.oauth_handler_with_secret.set_token_expiry_time(time.time() + 3600)
        
        valid_token = self.oauth_handler_with_secret.get_valid_access_token()
        self.assertEqual(valid_token, "valid-token")
    
    def test_get_valid_access_token_with_refresh(self):
        """Test getting valid access token with refresh."""
        self.oauth_handler_with_secret.set_access_token("expired-token")
        self.oauth_handler_with_secret.set_refresh_token("valid-refresh-token")
        self.oauth_handler_with_secret.set_token_expiry_time(time.time() - 3600)
        
        # Mock the refresh response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new-valid-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            valid_token = self.oauth_handler_with_secret.get_valid_access_token()
            self.assertEqual(valid_token, "new-valid-token")
    
    def test_get_valid_access_token_no_refresh_token(self):
        """Test getting valid access token without refresh token."""
        self.oauth_handler_with_secret.set_access_token("expired-token")
        self.oauth_handler_with_secret.set_token_expiry_time(time.time() - 3600)
        
        with self.assertRaises(ValueError) as context:
            self.oauth_handler_with_secret.get_valid_access_token()
        
        self.assertIn("Refresh token is not available", str(context.exception))
    
    def test_logout_success(self):
        """Test successful logout."""
        # Set up tokens
        self.oauth_handler_with_secret.set_access_token("test-token")
        self.oauth_handler_with_secret.set_refresh_token("test-refresh-token")
        
        # Mock the revoke response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            result = self.oauth_handler_with_secret.logout()
            
            self.assertTrue(result)
            self.assertIsNone(self.oauth_handler_with_secret.get_access_token())
            self.assertIsNone(self.oauth_handler_with_secret.get_refresh_token())
    
    def test_logout_without_revoke(self):
        """Test logout without revoking authorization."""
        # Set up tokens
        self.oauth_handler_with_secret.set_access_token("test-token")
        self.oauth_handler_with_secret.set_refresh_token("test-refresh-token")
        
        result = self.oauth_handler_with_secret.logout(revoke_authorization=False)
        
        self.assertTrue(result)
        self.assertIsNone(self.oauth_handler_with_secret.get_access_token())
        self.assertIsNone(self.oauth_handler_with_secret.get_refresh_token())
    
    # Note: Tests for get_oauth_app_authorization and revoke_oauth_app_authorization 
    # methods removed as these methods were removed from OAuthHandler for simplicity
    
    def test_getter_setter_methods(self):
        """Test all getter and setter methods."""
        # Test access token
        self.oauth_handler_with_secret.set_access_token("test-access-token")
        self.assertEqual(self.oauth_handler_with_secret.get_access_token(), "test-access-token")
        
        # Test refresh token
        self.oauth_handler_with_secret.set_refresh_token("test-refresh-token")
        self.assertEqual(self.oauth_handler_with_secret.get_refresh_token(), "test-refresh-token")
        
        # Test organization UID
        self.oauth_handler_with_secret.set_organization_uid("test-org-uid")
        self.assertEqual(self.oauth_handler_with_secret.get_organization_uid(), "test-org-uid")
        
        # Test user UID
        self.oauth_handler_with_secret.set_user_uid("test-user-uid")
        self.assertEqual(self.oauth_handler_with_secret.get_user_uid(), "test-user-uid")
        
        # Test token expiry time
        expiry_time = time.time() + 3600
        self.oauth_handler_with_secret.set_token_expiry_time(expiry_time)
        self.assertEqual(self.oauth_handler_with_secret.get_token_expiry_time(), expiry_time)


if __name__ == '__main__':
    unittest.main()
