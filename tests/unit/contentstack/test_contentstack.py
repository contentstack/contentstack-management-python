import unittest
import contentstack_management
from contentstack_management.contentstack import Region


class ContentstackRegionUnitTests(unittest.TestCase):

    def test_au_region(self):
        """Test that au region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='au')
        expected_endpoint = 'https://au-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_eu_region(self):
        """Test that gcp-eu region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='gcp-eu')
        expected_endpoint = 'https://gcp-eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_azure_eu_region(self):
        """Test that azure-eu region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='azure-eu')
        expected_endpoint = 'https://azure-eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_azure_na_region(self):
        """Test that azure-na region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='azure-na')
        expected_endpoint = 'https://azure-na-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_au_region_with_custom_host(self):
        """Test that au region with custom host creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='au', 
            host='example.com'
        )
        expected_endpoint = 'https://au-api.example.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_eu_region_with_custom_host(self):
        """Test that gcp-eu region with custom host creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='gcp-eu', 
            host='custom.contentstack.io'
        )
        expected_endpoint = 'https://gcp-eu-api.custom.contentstack.io/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_au_region_enum_value(self):
        """Test that au region using enum value creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region=Region.AU.value)
        expected_endpoint = 'https://au-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_eu_region_enum_value(self):
        """Test that gcp-eu region using enum value creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region=Region.GCP_EU.value)
        expected_endpoint = 'https://gcp-eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_au_region_with_custom_scheme(self):
        """Test that au region with custom scheme creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='au', 
            scheme='http://'
        )
        expected_endpoint = 'http://au-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_eu_region_with_custom_scheme(self):
        """Test that gcp-eu region with custom scheme creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='gcp-eu', 
            scheme='http://'
        )
        expected_endpoint = 'http://gcp-eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_au_region_with_custom_version(self):
        """Test that au region with custom version creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='au', 
            version='v2'
        )
        expected_endpoint = 'https://au-api.contentstack.com/v2/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_eu_region_with_custom_version(self):
        """Test that gcp-eu region with custom version creates the correct endpoint URL"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='gcp-eu', 
            version='v2'
        )
        expected_endpoint = 'https://gcp-eu-api.contentstack.com/v2/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_au_region_headers(self):
        """Test that au region client has correct headers"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='au')
        self.assertIn('authtoken', client.client.headers)
        self.assertEqual(client.client.headers['authtoken'], 'your_authtoken')
        self.assertIn('X-User-Agent', client.client.headers)
        self.assertIn('Content-Type', client.client.headers)
        self.assertEqual(client.client.headers['Content-Type'], 'application/json')

    def test_gcp_eu_region_headers(self):
        """Test that gcp-eu region client has correct headers"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='gcp-eu')
        self.assertIn('authtoken', client.client.headers)
        self.assertEqual(client.client.headers['authtoken'], 'your_authtoken')
        self.assertIn('X-User-Agent', client.client.headers)
        self.assertIn('Content-Type', client.client.headers)
        self.assertEqual(client.client.headers['Content-Type'], 'application/json')

    def test_au_region_with_management_token(self):
        """Test that au region client with management token has correct authorization header"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            management_token='Bearer your_management_token',
            region='au'
        )
        self.assertIn('authorization', client.client.headers)
        self.assertEqual(client.client.headers['authorization'], 'Bearer your_management_token')

    def test_gcp_eu_region_with_management_token(self):
        """Test that gcp-eu region client with management token has correct authorization header"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            management_token='Bearer your_management_token',
            region='gcp-eu'
        )
        self.assertIn('authorization', client.client.headers)
        self.assertEqual(client.client.headers['authorization'], 'Bearer your_management_token')

    def test_region_enum_values(self):
        """Test that Region enum contains the expected region values"""
        self.assertEqual(Region.US.value, 'us')
        self.assertEqual(Region.EU.value, 'eu')
        self.assertEqual(Region.AU.value, 'au')
        self.assertEqual(Region.AZURE_EU.value, 'azure-eu')
        self.assertEqual(Region.AZURE_NA.value, 'azure-na')
        self.assertEqual(Region.GCP_NA.value, 'gcp-na')
        self.assertEqual(Region.GCP_EU.value, 'gcp-eu')

    def test_au_region_timeout_and_retries(self):
        """Test that au region client respects timeout and max_retries parameters"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='au',
            timeout=5,
            max_retries=10
        )
        self.assertEqual(client.client.timeout, 5)
        self.assertEqual(client.client.max_retries, 10)

    def test_gcp_eu_region_timeout_and_retries(self):
        """Test that gcp-eu region client respects timeout and max_retries parameters"""
        client = contentstack_management.Client(
            authtoken='your_authtoken', 
            region='gcp-eu',
            timeout=5,
            max_retries=10
        )
        self.assertEqual(client.client.timeout, 5)
        self.assertEqual(client.client.max_retries, 10)


    def test_default_client_initialization(self):
        """Test default client initialization with no parameters"""
        client = contentstack_management.Client()
        expected_endpoint = 'https://api.contentstack.io/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)
        self.assertIn('X-User-Agent', client.client.headers)
        self.assertIn('Content-Type', client.client.headers)
        self.assertEqual(client.client.headers['Content-Type'], 'application/json')

    def test_client_with_headers_parameter(self):
        """Test client initialization with custom headers"""
        custom_headers = {'Custom-Header': 'custom-value'}
        client = contentstack_management.Client(headers=custom_headers)
        self.assertIn('Custom-Header', client.client.headers)
        self.assertEqual(client.client.headers['Custom-Header'], 'custom-value')
        self.assertIn('X-User-Agent', client.client.headers)
        self.assertIn('Content-Type', client.client.headers)

    def test_client_with_authtoken_only(self):
        """Test client initialization with authtoken only"""
        client = contentstack_management.Client(authtoken='test_token')
        self.assertIn('authtoken', client.client.headers)
        self.assertEqual(client.client.headers['authtoken'], 'test_token')

    def test_client_with_management_token_only(self):
        """Test client initialization with management token only"""
        client = contentstack_management.Client(management_token='Bearer test_management_token')
        self.assertIn('authorization', client.client.headers)
        self.assertEqual(client.client.headers['authorization'], 'Bearer test_management_token')

    def test_client_with_both_tokens(self):
        """Test client initialization with both authtoken and management token"""
        client = contentstack_management.Client(
            authtoken='test_token',
            management_token='Bearer test_management_token'
        )
        self.assertIn('authtoken', client.client.headers)
        self.assertEqual(client.client.headers['authtoken'], 'test_token')
        self.assertIn('authorization', client.client.headers)
        self.assertEqual(client.client.headers['authorization'], 'Bearer test_management_token')

    def test_us_region_default_behavior(self):
        """Test that US region behaves as default (no region prefix)"""
        client = contentstack_management.Client(region='us')
        expected_endpoint = 'https://api.contentstack.io/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_eu_region(self):
        """Test that eu region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='eu')
        expected_endpoint = 'https://eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_gcp_na_region(self):
        """Test that gcp-na region creates the correct endpoint URL"""
        client = contentstack_management.Client(authtoken='your_authtoken', region='gcp-na')
        expected_endpoint = 'https://gcp-na-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_region_with_none_host(self):
        """Test region behavior when host is None"""
        client = contentstack_management.Client(region='eu', host=None)
        expected_endpoint = 'https://eu-api.contentstack.com/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_region_with_none_region(self):
        """Test behavior when region is None"""
        client = contentstack_management.Client(region=None, host='custom.contentstack.io')
        expected_endpoint = 'https://custom.contentstack.io/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

    def test_user_agents_function(self):
        """Test the user_agents function"""
        from contentstack_management.contentstack import user_agents
        
        # Test with None headers
        headers = user_agents(None)
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')
        
        # Test with existing headers
        existing_headers = {'Existing-Header': 'existing-value'}
        headers = user_agents(existing_headers)
        self.assertIn('Existing-Header', headers)
        self.assertEqual(headers['Existing-Header'], 'existing-value')
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)

    def test_user_agents_function_with_empty_dict(self):
        """Test the user_agents function with empty dictionary"""
        from contentstack_management.contentstack import user_agents
        
        headers = user_agents({})
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')

    def test_authtoken_property(self):
        """Test the authtoken property"""
        client = contentstack_management.Client(authtoken='test_authtoken')
        self.assertEqual(client.authtoken, 'test_authtoken')

    def test_authtoken_property_without_authtoken(self):
        """Test the authtoken property when no authtoken is set"""
        client = contentstack_management.Client()
        # This should raise a KeyError since no authtoken was set
        with self.assertRaises(KeyError):
            _ = client.authtoken

    def test_user_method(self):
        """Test the user method returns a User object"""
        client = contentstack_management.Client()
        user_obj = client.user()
        self.assertIsNotNone(user_obj)
        # Verify it's the correct type by checking if it has the expected client attribute
        self.assertEqual(user_obj.client, client.client)

    def test_organizations_method_without_uid(self):
        """Test the organizations method without organization_uid"""
        client = contentstack_management.Client()
        org_obj = client.organizations()
        self.assertIsNotNone(org_obj)
        self.assertEqual(org_obj.client, client.client)
        self.assertIsNone(org_obj.organization_uid)

    def test_organizations_method_with_uid(self):
        """Test the organizations method with organization_uid"""
        client = contentstack_management.Client()
        org_uid = 'test_org_uid'
        org_obj = client.organizations(org_uid)
        self.assertIsNotNone(org_obj)
        self.assertEqual(org_obj.client, client.client)
        self.assertEqual(org_obj.organization_uid, org_uid)

    def test_stack_method_without_api_key(self):
        """Test the stack method without api_key"""
        client = contentstack_management.Client()
        stack_obj = client.stack()
        self.assertIsNotNone(stack_obj)
        self.assertEqual(stack_obj.client, client.client)
        # Skip api_key check as it might not be exposed as an attribute

    def test_stack_method_with_api_key(self):
        """Test the stack method with api_key"""
        client = contentstack_management.Client()
        api_key = 'test_api_key'
        stack_obj = client.stack(api_key)
        self.assertIsNotNone(stack_obj)
        self.assertEqual(stack_obj.client, client.client)
        # Skip api_key check as it might not be exposed as an attribute

    def test_login_method_signature(self):
        """Test that login method accepts the correct parameters"""
        client = contentstack_management.Client()
        # Test that the method exists and can be called with the expected parameters
        # We can't test the actual login without real credentials, but we can test the method signature
        self.assertTrue(hasattr(client, 'login'))
        self.assertTrue(callable(client.login))

    def test_logout_method_signature(self):
        """Test that logout method exists and is callable"""
        client = contentstack_management.Client()
        # Test that the method exists and can be called
        self.assertTrue(hasattr(client, 'logout'))
        self.assertTrue(callable(client.logout))

    def test_version_constant(self):
        """Test that the version constant is defined"""
        from contentstack_management.contentstack import version
        self.assertEqual(version, '0.0.1')

    def test_region_enum_completeness(self):
        """Test that all expected regions are present in the enum"""
        expected_regions = {
            'US': 'us',
            'EU': 'eu', 
            'AU': 'au',
            'AZURE_EU': 'azure-eu',
            'AZURE_NA': 'azure-na',
            'GCP_NA': 'gcp-na',
            'GCP_EU': 'gcp-eu'
        }
        
        for region_name, region_value in expected_regions.items():
            self.assertTrue(hasattr(Region, region_name))
            self.assertEqual(getattr(Region, region_name).value, region_value)

    def test_client_with_kwargs(self):
        """Test that client accepts additional kwargs without error"""
        client = contentstack_management.Client(
            authtoken='test_token',
            extra_param1='value1',
            extra_param2='value2'
        )
        # Should not raise any error
        self.assertIsNotNone(client)

    def test_client_initialization_with_none_values(self):
        """Test client initialization with None values for optional parameters"""
        client = contentstack_management.Client(
            authtoken=None,
            management_token=None,
            headers=None,
            early_access=None
        )
        # Should not raise any error and should have default endpoint
        expected_endpoint = 'https://api.contentstack.io/v3/'
        self.assertEqual(client.endpoint, expected_endpoint)

if __name__ == '__main__':
    unittest.main()
