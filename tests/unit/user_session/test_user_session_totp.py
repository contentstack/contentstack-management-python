import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Add the contentstack_management module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from contentstack_management.user_session.user_session import UserSession


class UserSessionTOTPTests(unittest.TestCase):
    """Unit tests for TOTP-related functionality in UserSession class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_client = MagicMock()
        self.user_session = UserSession(self.mock_client)
        self.test_email = "test@example.com"
        self.test_password = "test_password"
        self.test_tfa_token = "123456"

    def test_login_with_tfa_token_uses_correct_field_name(self):
        """Test that login with TFA token uses 'tfa_token' field name (not 'tf_token')"""
        # Mock the client post method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
        self.mock_client.post.return_value = mock_response
        
        # Call login with TFA token
        result = self.user_session.login(self.test_email, self.test_password, self.test_tfa_token)
        
        # Verify the request was made correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        
        # Check the data - this is the critical test for the field name fix
        expected_data = {
            "user": {
                "email": self.test_email,
                "password": self.test_password,
                "tfa_token": self.test_tfa_token  # Should be "tfa_token", not "tf_token"
            }
        }
        actual_data = json.loads(call_args[1]['data'])
        self.assertEqual(actual_data, expected_data)
        
        # Verify the correct field name is used
        self.assertIn("tfa_token", actual_data["user"])
        self.assertNotIn("tf_token", actual_data["user"])
        self.assertEqual(actual_data["user"]["tfa_token"], self.test_tfa_token)
        
        # Check the response
        self.assertEqual(result, mock_response)

    def test_login_without_tfa_token(self):
        """Test login without TFA token (original behavior)"""
        # Mock the client post method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
        self.mock_client.post.return_value = mock_response
        
        # Call login without TFA token
        result = self.user_session.login(self.test_email, self.test_password)
        
        # Verify the request was made correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        
        # Check the data
        expected_data = {
            "user": {
                "email": self.test_email,
                "password": self.test_password
            }
        }
        actual_data = json.loads(call_args[1]['data'])
        self.assertEqual(actual_data, expected_data)
        
        # Check the response
        self.assertEqual(result, mock_response)

    def test_login_with_none_tfa_token(self):
        """Test login with None TFA token"""
        # Mock the client post method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'user': {'authtoken': 'test_token'}}
        self.mock_client.post.return_value = mock_response
        
        # Call login with None TFA token
        result = self.user_session.login(self.test_email, self.test_password, None)
        
        # Verify the request was made correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        
        # Check the data - None should not be included
        expected_data = {
            "user": {
                "email": self.test_email,
                "password": self.test_password
            }
        }
        actual_data = json.loads(call_args[1]['data'])
        self.assertEqual(actual_data, expected_data)
        
        # Check the response
        self.assertEqual(result, mock_response)

    def test_login_parameter_validation(self):
        """Test login parameter validation"""
        # Test with empty email
        with self.assertRaises(PermissionError) as context:
            self.user_session.login("", self.test_password, self.test_tfa_token)
        self.assertIn("Email Id is required", str(context.exception))
        
        # Test with empty password
        with self.assertRaises(PermissionError) as context:
            self.user_session.login(self.test_email, "", self.test_tfa_token)
        self.assertIn("Password is required", str(context.exception))

    def test_login_method_signature(self):
        """Test that login method has the correct signature"""
        import inspect
        
        # Get the signature of the login method
        sig = inspect.signature(self.user_session.login)
        params = list(sig.parameters.keys())
        
        # Verify the method has the expected parameters
        expected_params = ['email', 'password', 'tfa_token']
        for param in expected_params:
            self.assertIn(param, params)
        
        # Verify parameter defaults
        self.assertEqual(sig.parameters['tfa_token'].default, None)


if __name__ == '__main__':
    unittest.main()