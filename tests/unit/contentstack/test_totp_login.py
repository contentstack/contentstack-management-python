import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the contentstack_management module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import contentstack_management
from contentstack_management.contentstack import Client


class TOTPLoginTests(unittest.TestCase):
    """Unit tests for TOTP login functionality in Contentstack Management Python SDK"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.client = Client()
        self.test_email = "test@example.com"
        self.test_password = "test_password"
        self.test_secret = "JBSWY3DPEHPK3PXP"  # Standard test secret for TOTP
        self.test_tfa_token = "123456"

    def tearDown(self):
        """Clean up after each test method"""
        # Clean up environment variables
        if 'MFA_SECRET' in os.environ:
            del os.environ['MFA_SECRET']

    def test_login_method_signature_with_totp(self):
        """Test that login method accepts TOTP parameters"""
        client = contentstack_management.Client()
        # Test that the method exists and can be called with the expected parameters
        self.assertTrue(hasattr(client, 'login'))
        self.assertTrue(callable(client.login))
        
        # Test that the method accepts TOTP parameters without error
        try:
            client.login(self.test_email, self.test_password, tfa_token=self.test_tfa_token)
            client.login(self.test_email, self.test_password, mfa_secret=self.test_secret)
            client.login(self.test_email, self.test_password, tfa_token=self.test_tfa_token, mfa_secret=self.test_secret)
        except Exception as e:
            self.fail(f"Login method should accept TOTP parameters without error: {e}")

    def test_generate_totp_method(self):
        """Test the _generate_totp method generates correct TOTP codes"""
        # Test with a known secret and verify the TOTP generation
        totp_code = self.client._generate_totp(self.test_secret)
        
        # Verify the TOTP code is a 6-digit string
        self.assertIsInstance(totp_code, str)
        self.assertEqual(len(totp_code), 6)
        self.assertTrue(totp_code.isdigit())

    def test_login_with_mfa_secret_generates_totp(self):
        """Test that login with mfa_secret generates TOTP automatically"""
        with patch.object(self.client, 'client') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
            mock_client.post.return_value = mock_response
            
            # Mock the UserSession class
            with patch('contentstack_management.user_session.user_session.UserSession') as mock_user_session:
                mock_session_instance = MagicMock()
                mock_session_instance.login.return_value = mock_response
                mock_user_session.return_value = mock_session_instance
                
                # Mock the _generate_totp method to return a predictable value
                with patch.object(self.client, '_generate_totp', return_value='654321') as mock_generate_totp:
                    result = self.client.login(
                        self.test_email, 
                        self.test_password, 
                        mfa_secret=self.test_secret
                    )
                    
                    # Verify _generate_totp was called with the secret
                    mock_generate_totp.assert_called_once_with(self.test_secret)
                    
                    # Verify UserSession was called with generated TOTP
                    mock_session_instance.login.assert_called_once_with(
                        self.test_email, 
                        self.test_password, 
                        '654321'
                    )
                    self.assertEqual(result, mock_response)

    def test_login_with_environment_variable(self):
        """Test that login uses MFA_SECRET environment variable when mfa_secret is not provided"""
        # Set environment variable
        os.environ['MFA_SECRET'] = self.test_secret
        
        with patch.object(self.client, 'client') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
            mock_client.post.return_value = mock_response
            
            # Mock the UserSession class
            with patch('contentstack_management.user_session.user_session.UserSession') as mock_user_session:
                mock_session_instance = MagicMock()
                mock_session_instance.login.return_value = mock_response
                mock_user_session.return_value = mock_session_instance
                
                # Mock the _generate_totp method
                with patch.object(self.client, '_generate_totp', return_value='789012') as mock_generate_totp:
                    result = self.client.login(self.test_email, self.test_password)
                    
                    # Verify _generate_totp was called with the environment secret
                    mock_generate_totp.assert_called_once_with(self.test_secret)
                    
                    # Verify UserSession was called with generated TOTP
                    mock_session_instance.login.assert_called_once_with(
                        self.test_email, 
                        self.test_password, 
                        '789012'
                    )
                    self.assertEqual(result, mock_response)

    def test_backward_compatibility(self):
        """Test that existing login patterns continue to work (backward compatibility)"""
        with patch.object(self.client, 'client') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
            mock_client.post.return_value = mock_response
            
            # Mock the UserSession class
            with patch('contentstack_management.user_session.user_session.UserSession') as mock_user_session:
                mock_session_instance = MagicMock()
                mock_session_instance.login.return_value = mock_response
                mock_user_session.return_value = mock_session_instance
                
                # Test old pattern: client.login(email, password)
                result1 = self.client.login(self.test_email, self.test_password)
                
                # Test old pattern: client.login(email, password, tfa_token)
                result2 = self.client.login(self.test_email, self.test_password, self.test_tfa_token)
                
                # Both should work without errors
                self.assertEqual(result1, mock_response)
                self.assertEqual(result2, mock_response)


if __name__ == '__main__':
    unittest.main()