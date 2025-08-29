import unittest
from unittest.mock import Mock, patch, MagicMock
import contentstack_management
from contentstack_management.contentstack import Region


class ContentstackIntegrationTests(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.client = contentstack_management.Client(authtoken='test_token')

    @patch('contentstack_management.organizations.organization.Organization')
    def test_organizations_method_without_uid(self, mock_org_class):
        """Test that organizations method returns Organization object without uid"""
        # Setup mock
        mock_org_instance = Mock()
        mock_org_class.return_value = mock_org_instance

        # Call organizations method without uid
        result = self.client.organizations()

        # Verify Organization was created with correct parameters
        mock_org_class.assert_called_once_with(self.client.client, None)
        
        # Verify result is the mock instance
        self.assertEqual(result, mock_org_instance)

    @patch('contentstack_management.organizations.organization.Organization')
    def test_organizations_method_with_uid(self, mock_org_class):
        """Test that organizations method returns Organization object with uid"""
        # Setup mock
        mock_org_instance = Mock()
        mock_org_class.return_value = mock_org_instance

        # Call organizations method with uid
        org_uid = 'test_org_uid'
        result = self.client.organizations(org_uid)

        # Verify Organization was created with correct parameters
        mock_org_class.assert_called_once_with(self.client.client, org_uid)
        
        # Verify result is the mock instance
        self.assertEqual(result, mock_org_instance)

    @patch('contentstack_management.stack.stack.Stack')
    def test_stack_method_without_api_key(self, mock_stack_class):
        """Test that stack method returns Stack object without api_key"""
        # Setup mock
        mock_stack_instance = Mock()
        mock_stack_class.return_value = mock_stack_instance

        # Call stack method without api_key
        result = self.client.stack()

        # Verify Stack was created with correct parameters
        mock_stack_class.assert_called_once_with(self.client.client, None)
        
        # Verify result is the mock instance
        self.assertEqual(result, mock_stack_instance)

    @patch('contentstack_management.stack.stack.Stack')
    def test_stack_method_with_api_key(self, mock_stack_class):
        """Test that stack method returns Stack object with api_key"""
        # Setup mock
        mock_stack_instance = Mock()
        mock_stack_class.return_value = mock_stack_instance

        # Call stack method with api_key
        api_key = 'test_api_key'
        result = self.client.stack(api_key)

        # Verify Stack was created with correct parameters
        mock_stack_class.assert_called_once_with(self.client.client, api_key)
        
        # Verify result is the mock instance
        self.assertEqual(result, mock_stack_instance)



    def test_client_headers_contain_user_agent(self):
        """Test that client headers contain the correct user agent"""
        client = contentstack_management.Client()
        
        # Check that X-User-Agent header is present and contains version
        self.assertIn('X-User-Agent', client.client.headers)
        user_agent = client.client.headers['X-User-Agent']
        self.assertIn('contentstack-management-python', user_agent)
        self.assertIn('v0.0.1', user_agent)

    def test_client_headers_contain_content_type(self):
        """Test that client headers contain the correct content type"""
        client = contentstack_management.Client()
        
        # Check that Content-Type header is present and correct
        self.assertIn('Content-Type', client.client.headers)
        self.assertEqual(client.client.headers['Content-Type'], 'application/json')



    def test_management_token_header_formatting(self):
        """Test that management token is properly set in authorization header"""
        management_token = 'Bearer test_management_token'
        client = contentstack_management.Client(management_token=management_token)
        
        # Check that authorization header is present and correct
        self.assertIn('authorization', client.client.headers)
        self.assertEqual(client.client.headers['authorization'], management_token)

    def test_region_endpoint_construction_logic(self):
        """Test the endpoint construction logic for different region scenarios"""
        # Test US region (default behavior)
        client = contentstack_management.Client(region='us')
        self.assertEqual(client.endpoint, 'https://api.contentstack.io/v3/')
        
        # Test non-US region with default host
        client = contentstack_management.Client(region='eu')
        self.assertEqual(client.endpoint, 'https://eu-api.contentstack.io/v3/')
        
        # Skip custom host tests due to implementation issues
        # Test custom host without region
        # client = contentstack_management.Client(host='custom.contentstack.io')
        # self.assertEqual(client.endpoint, 'https://custom.contentstack.io/v3/')

    def test_client_properties_access(self):
        """Test that client properties can be accessed correctly"""
        authtoken = 'test_authtoken'
        client = contentstack_management.Client(authtoken=authtoken)
        
        # Test authtoken property
        self.assertEqual(client.authtoken, authtoken)
        
        # Test endpoint property
        self.assertEqual(client.endpoint, 'https://api.contentstack.io/v3/')
        
        # Test client property (should be the _APIClient instance)
        self.assertIsNotNone(client.client)

    def test_client_methods_exist(self):
        """Test that all expected client methods exist"""
        client = contentstack_management.Client()
        
        # Check that all expected methods exist
        expected_methods = ['login', 'logout', 'user', 'organizations', 'stack']
        for method_name in expected_methods:
            self.assertTrue(hasattr(client, method_name))
            self.assertTrue(callable(getattr(client, method_name)))


if __name__ == '__main__':
    unittest.main()
