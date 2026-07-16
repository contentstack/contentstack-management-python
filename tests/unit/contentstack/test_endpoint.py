import unittest

import contentstack_management
from contentstack_management.endpoint import Endpoint
from contentstack_management.contentstack import Region, Client

AUTHTOKEN = 'test_authtoken'


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        Endpoint.reset_cache()

    # -------------------------------------------------------------------------
    # Default region (us / na)
    # -------------------------------------------------------------------------

    def test_default_region_returns_all_endpoints(self):
        endpoints = Endpoint.get_contentstack_endpoint()
        self.assertIsInstance(endpoints, dict)
        self.assertIn('contentDelivery', endpoints)
        self.assertIn('contentManagement', endpoints)

    def test_default_region_content_management(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_default_region_content_delivery(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    # -------------------------------------------------------------------------
    # All 7 regions — contentManagement spot-checks (primary service for Mgmt SDK)
    # -------------------------------------------------------------------------

    def test_content_management_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_content_management_eu(self):
        url = Endpoint.get_contentstack_endpoint('eu', 'contentManagement')
        self.assertEqual('https://eu-api.contentstack.com', url)

    def test_content_management_au(self):
        url = Endpoint.get_contentstack_endpoint('au', 'contentManagement')
        self.assertEqual('https://au-api.contentstack.com', url)

    def test_content_management_azure_na(self):
        url = Endpoint.get_contentstack_endpoint('azure-na', 'contentManagement')
        self.assertEqual('https://azure-na-api.contentstack.com', url)

    def test_content_management_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint('azure-eu', 'contentManagement')
        self.assertEqual('https://azure-eu-api.contentstack.com', url)

    def test_content_management_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint('gcp-na', 'contentManagement')
        self.assertEqual('https://gcp-na-api.contentstack.com', url)

    def test_content_management_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint('gcp-eu', 'contentManagement')
        self.assertEqual('https://gcp-eu-api.contentstack.com', url)

    # -------------------------------------------------------------------------
    # All 7 regions — contentDelivery spot-checks
    # -------------------------------------------------------------------------

    def test_content_delivery_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_content_delivery_eu(self):
        url = Endpoint.get_contentstack_endpoint('eu', 'contentDelivery')
        self.assertEqual('https://eu-cdn.contentstack.com', url)

    def test_content_delivery_au(self):
        url = Endpoint.get_contentstack_endpoint('au', 'contentDelivery')
        self.assertEqual('https://au-cdn.contentstack.com', url)

    def test_content_delivery_azure_na(self):
        url = Endpoint.get_contentstack_endpoint('azure-na', 'contentDelivery')
        self.assertEqual('https://azure-na-cdn.contentstack.com', url)

    def test_content_delivery_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint('azure-eu', 'contentDelivery')
        self.assertEqual('https://azure-eu-cdn.contentstack.com', url)

    def test_content_delivery_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint('gcp-na', 'contentDelivery')
        self.assertEqual('https://gcp-na-cdn.contentstack.com', url)

    def test_content_delivery_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint('gcp-eu', 'contentDelivery')
        self.assertEqual('https://gcp-eu-cdn.contentstack.com', url)

    # -------------------------------------------------------------------------
    # NA aliases all resolve to the same endpoint
    # -------------------------------------------------------------------------

    def test_alias_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_us(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_aws_na_hyphen(self):
        url = Endpoint.get_contentstack_endpoint('aws-na', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_aws_na_underscore(self):
        url = Endpoint.get_contentstack_endpoint('aws_na', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_na_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('NA', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_us_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('US', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    # -------------------------------------------------------------------------
    # Case-insensitive alias matching for other regions
    # -------------------------------------------------------------------------

    def test_alias_aws_na_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('AWS-NA', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_alias_azure_na_underscore(self):
        url = Endpoint.get_contentstack_endpoint('azure_na', 'contentManagement')
        self.assertEqual('https://azure-na-api.contentstack.com', url)

    def test_alias_gcp_eu_underscore(self):
        url = Endpoint.get_contentstack_endpoint('gcp_eu', 'contentManagement')
        self.assertEqual('https://gcp-eu-api.contentstack.com', url)

    # -------------------------------------------------------------------------
    # Region enum constants resolve correctly
    # -------------------------------------------------------------------------

    def test_region_constant_us(self):
        url = Endpoint.get_contentstack_endpoint(Region.US.value, 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_region_constant_eu(self):
        url = Endpoint.get_contentstack_endpoint(Region.EU.value, 'contentManagement')
        self.assertEqual('https://eu-api.contentstack.com', url)

    def test_region_constant_au(self):
        url = Endpoint.get_contentstack_endpoint(Region.AU.value, 'contentManagement')
        self.assertEqual('https://au-api.contentstack.com', url)

    def test_region_constant_azure_na(self):
        url = Endpoint.get_contentstack_endpoint(Region.AZURE_NA.value, 'contentManagement')
        self.assertEqual('https://azure-na-api.contentstack.com', url)

    def test_region_constant_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint(Region.AZURE_EU.value, 'contentManagement')
        self.assertEqual('https://azure-eu-api.contentstack.com', url)

    def test_region_constant_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint(Region.GCP_NA.value, 'contentManagement')
        self.assertEqual('https://gcp-na-api.contentstack.com', url)

    def test_region_constant_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint(Region.GCP_EU.value, 'contentManagement')
        self.assertEqual('https://gcp-eu-api.contentstack.com', url)

    # -------------------------------------------------------------------------
    # omit_https flag
    # -------------------------------------------------------------------------

    def test_omit_https_strips_scheme_single_service(self):
        host = Endpoint.get_contentstack_endpoint('eu', 'contentManagement', omit_https=True)
        self.assertEqual('eu-api.contentstack.com', host)

    def test_omit_https_strips_scheme_all_services(self):
        endpoints = Endpoint.get_contentstack_endpoint('na', omit_https=True)
        self.assertIsInstance(endpoints, dict)
        for key, url in endpoints.items():
            self.assertNotIn('https://', url, f'Service {key} still has https://')
            self.assertNotIn('http://', url, f'Service {key} still has http://')

    def test_omit_https_false_retains_scheme(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentManagement', omit_https=False)
        self.assertTrue(url.startswith('https://'))

    # -------------------------------------------------------------------------
    # No service — returns full dict
    # -------------------------------------------------------------------------

    def test_no_service_returns_dict(self):
        result = Endpoint.get_contentstack_endpoint('au')
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 1)

    def test_no_service_contains_correct_urls(self):
        endpoints = Endpoint.get_contentstack_endpoint('au')
        self.assertEqual('https://au-cdn.contentstack.com', endpoints['contentDelivery'])
        self.assertEqual('https://au-api.contentstack.com', endpoints['contentManagement'])

    # -------------------------------------------------------------------------
    # Error cases
    # -------------------------------------------------------------------------

    def test_empty_region_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('')
        self.assertIn('Empty region', str(ctx.exception))

    def test_unknown_region_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('invalid-region')
        self.assertIn('Invalid region', str(ctx.exception))

    def test_unknown_service_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('na', 'unknownService')
        self.assertIn('unknownService', str(ctx.exception))

    # -------------------------------------------------------------------------
    # contentstack_management.get_contentstack_endpoint() module-level proxy
    # -------------------------------------------------------------------------

    def test_module_proxy_returns_same_result(self):
        via_class = Endpoint.get_contentstack_endpoint('eu', 'contentManagement')
        via_module = contentstack_management.get_contentstack_endpoint('eu', 'contentManagement')
        self.assertEqual(via_class, via_module)

    def test_module_proxy_default_region(self):
        url = contentstack_management.get_contentstack_endpoint('us', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_module_proxy_omit_https(self):
        host = contentstack_management.get_contentstack_endpoint(
            'gcp-na', 'contentManagement', omit_https=True)
        self.assertEqual('gcp-na-api.contentstack.com', host)

    def test_module_proxy_all_endpoints(self):
        endpoints = contentstack_management.get_contentstack_endpoint('azure-eu')
        self.assertIsInstance(endpoints, dict)
        self.assertIn('contentManagement', endpoints)

    # -------------------------------------------------------------------------
    # Client endpoint resolution via Endpoint
    # -------------------------------------------------------------------------

    def test_client_us_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region=Region.US.value)
        self.assertEqual('https://api.contentstack.io/v3/', client.endpoint)

    def test_client_eu_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='eu')
        self.assertEqual('https://eu-api.contentstack.com/v3/', client.endpoint)

    def test_client_au_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='au')
        self.assertEqual('https://au-api.contentstack.com/v3/', client.endpoint)

    def test_client_azure_na_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='azure-na')
        self.assertEqual('https://azure-na-api.contentstack.com/v3/', client.endpoint)

    def test_client_azure_eu_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='azure-eu')
        self.assertEqual('https://azure-eu-api.contentstack.com/v3/', client.endpoint)

    def test_client_gcp_na_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='gcp-na')
        self.assertEqual('https://gcp-na-api.contentstack.com/v3/', client.endpoint)

    def test_client_gcp_eu_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='gcp-eu')
        self.assertEqual('https://gcp-eu-api.contentstack.com/v3/', client.endpoint)

    def test_client_region_enum_value_au(self):
        client = Client(authtoken=AUTHTOKEN, region=Region.AU.value)
        self.assertEqual('https://au-api.contentstack.com/v3/', client.endpoint)

    def test_client_custom_host_overrides_endpoint(self):
        client = Client(authtoken=AUTHTOKEN, region='au', host='example.com')
        self.assertEqual('https://au-api.example.com/v3/', client.endpoint)

    def test_client_custom_host_us_region(self):
        client = Client(authtoken=AUTHTOKEN, host='custom.contentstack.io')
        self.assertEqual('https://custom.contentstack.io/v3/', client.endpoint)

    def test_client_default_us_no_region(self):
        client = Client(authtoken=AUTHTOKEN)
        self.assertEqual('https://api.contentstack.io/v3/', client.endpoint)


if __name__ == '__main__':
    unittest.main()
