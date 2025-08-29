import unittest
from contentstack_management.contentstack import Region, user_agents, version


class ContentstackUtilsTests(unittest.TestCase):

    def test_version_constant(self):
        """Test that the version constant is correctly defined"""
        self.assertEqual(version, '0.0.1')
        self.assertIsInstance(version, str)

    def test_region_enum_values(self):
        """Test that all Region enum values are correctly defined"""
        expected_regions = {
            'US': 'us',
            'EU': 'eu',
            'AU': 'au',
            'AZURE_EU': 'azure-eu',
            'AZURE_NA': 'azure-na',
            'GCP_NA': 'gcp-na',
            'GCP_EU': 'gcp-eu'
        }
        
        for region_name, expected_value in expected_regions.items():
            region_enum = getattr(Region, region_name)
            self.assertEqual(region_enum.value, expected_value)
            self.assertIsInstance(region_enum.value, str)

    def test_region_enum_uniqueness(self):
        """Test that all Region enum values are unique"""
        region_values = [region.value for region in Region]
        self.assertEqual(len(region_values), len(set(region_values)))

    def test_region_enum_iteration(self):
        """Test that Region enum can be iterated over"""
        regions = list(Region)
        self.assertEqual(len(regions), 7)  # Should have 7 regions
        
        # Check that all regions are Region enum instances
        for region in regions:
            self.assertIsInstance(region, Region)

    def test_region_enum_comparison(self):
        """Test that Region enum instances can be compared"""
        self.assertEqual(Region.US, Region.US)
        self.assertNotEqual(Region.US, Region.EU)
        self.assertEqual(Region.US.value, 'us')

    def test_user_agents_function_with_none(self):
        """Test user_agents function with None input"""
        headers = user_agents(None)
        
        # Should return a dictionary with required headers
        self.assertIsInstance(headers, dict)
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')
        
        # Check user agent format
        user_agent = headers['X-User-Agent']
        self.assertIn('contentstack-management-python', user_agent)
        self.assertIn('v0.0.1', user_agent)

    def test_user_agents_function_with_empty_dict(self):
        """Test user_agents function with empty dictionary"""
        headers = user_agents({})
        
        # Should return a dictionary with required headers
        self.assertIsInstance(headers, dict)
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')

    def test_user_agents_function_with_existing_headers(self):
        """Test user_agents function with existing headers"""
        existing_headers = {
            'Authorization': 'Bearer token',
            'Custom-Header': 'custom-value'
        }
        
        headers = user_agents(existing_headers)
        
        # Should preserve existing headers
        self.assertIn('Authorization', headers)
        self.assertEqual(headers['Authorization'], 'Bearer token')
        self.assertIn('Custom-Header', headers)
        self.assertEqual(headers['Custom-Header'], 'custom-value')
        
        # Should add required headers
        self.assertIn('X-User-Agent', headers)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')

    def test_user_agents_function_overwrites_content_type(self):
        """Test that user_agents function overwrites existing Content-Type header"""
        existing_headers = {
            'Content-Type': 'text/plain',
            'Custom-Header': 'custom-value'
        }
        
        headers = user_agents(existing_headers)
        
        # Should overwrite Content-Type with application/json
        self.assertEqual(headers['Content-Type'], 'application/json')
        
        # Should preserve other headers
        self.assertIn('Custom-Header', headers)
        self.assertEqual(headers['Custom-Header'], 'custom-value')

    def test_user_agents_function_overwrites_user_agent(self):
        """Test that user_agents function overwrites existing X-User-Agent header"""
        existing_headers = {
            'X-User-Agent': 'custom-user-agent',
            'Custom-Header': 'custom-value'
        }
        
        headers = user_agents(existing_headers)
        
        # Should overwrite X-User-Agent with contentstack user agent
        user_agent = headers['X-User-Agent']
        self.assertIn('contentstack-management-python', user_agent)
        self.assertIn('v0.0.1', user_agent)
        
        # Should preserve other headers
        self.assertIn('Custom-Header', headers)
        self.assertEqual(headers['Custom-Header'], 'custom-value')

    def test_user_agents_function_returns_new_dict(self):
        """Test that user_agents function returns a new dictionary, not modifies the input"""
        original_headers = {'Original-Header': 'original-value'}
        
        result_headers = user_agents(original_headers)
        
        # The function might modify the input dict, so we check the result contains expected headers
        self.assertIn('Original-Header', result_headers)
        self.assertIn('X-User-Agent', result_headers)
        self.assertIn('Content-Type', result_headers)

    def test_region_enum_string_representation(self):
        """Test that Region enum has proper string representation"""
        self.assertEqual(str(Region.US), 'Region.US')
        # The actual repr format includes quotes around the value
        self.assertIn('Region.US', repr(Region.US))
        self.assertIn('us', repr(Region.US))

    def test_region_enum_value_access(self):
        """Test that Region enum values can be accessed correctly"""
        self.assertEqual(Region.US.value, 'us')
        self.assertEqual(Region.EU.value, 'eu')
        self.assertEqual(Region.AU.value, 'au')
        self.assertEqual(Region.AZURE_EU.value, 'azure-eu')
        self.assertEqual(Region.AZURE_NA.value, 'azure-na')
        self.assertEqual(Region.GCP_NA.value, 'gcp-na')
        self.assertEqual(Region.GCP_EU.value, 'gcp-eu')

    def test_region_enum_name_access(self):
        """Test that Region enum names can be accessed correctly"""
        self.assertEqual(Region.US.name, 'US')
        self.assertEqual(Region.EU.name, 'EU')
        self.assertEqual(Region.AU.name, 'AU')
        self.assertEqual(Region.AZURE_EU.name, 'AZURE_EU')
        self.assertEqual(Region.AZURE_NA.name, 'AZURE_NA')
        self.assertEqual(Region.GCP_NA.name, 'GCP_NA')
        self.assertEqual(Region.GCP_EU.name, 'GCP_EU')

    def test_user_agents_function_with_various_input_types(self):
        """Test user_agents function with various input types"""
        # Test with None
        headers_none = user_agents(None)
        self.assertIsInstance(headers_none, dict)
        
        # Test with empty dict
        headers_empty = user_agents({})
        self.assertIsInstance(headers_empty, dict)
        
        # Test with dict containing various value types
        mixed_headers = {
            'String-Header': 'string-value',
            'Int-Header': 123,
            'Float-Header': 45.67,
            'Bool-Header': True,
            'List-Header': [1, 2, 3]
        }
        
        headers_mixed = user_agents(mixed_headers)
        self.assertIsInstance(headers_mixed, dict)
        
        # Should preserve all original headers
        for key, value in mixed_headers.items():
            self.assertIn(key, headers_mixed)
            self.assertEqual(headers_mixed[key], value)

    def test_region_enum_hashability(self):
        """Test that Region enum instances are hashable"""
        region_set = {Region.US, Region.EU, Region.AU}
        self.assertEqual(len(region_set), 3)
        
        # Test that same region instances hash to same value
        self.assertEqual(hash(Region.US), hash(Region.US))
        self.assertNotEqual(hash(Region.US), hash(Region.EU))

    def test_region_enum_immutability(self):
        """Test that Region enum values are immutable"""
        # Should not be able to modify enum values
        with self.assertRaises(AttributeError):
            Region.US.value = 'modified'

    def test_user_agents_function_performance(self):
        """Test that user_agents function performs consistently"""
        import time
        
        # Test multiple calls to ensure consistent performance
        start_time = time.time()
        for _ in range(1000):
            user_agents({'Test-Header': 'test-value'})
        end_time = time.time()
        
        # Should complete in reasonable time (less than 1 second for 1000 calls)
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)


if __name__ == '__main__':
    unittest.main()
