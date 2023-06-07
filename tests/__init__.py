# pytest --html=tests/report/test-report.html 
# above command runs tests and test reports generates in tests/report location.
# nosetests --with-coverage --cover-html
# clean all the .pyc files
# find . -name \*.pyc -delete
# nosetests --with-coverage --cover-html
# pytest --cov=contentstack
# pytest -v --cov=contentstack --cov-report=html
# pytest --html=tests/report/test-report.html
import unittest
from unittest import TestLoader, TestSuite

from .users.test_api import UserApiTests
from .users.test_mock import UserMockTests
from .users.test_unittest import UserUnitTests

from .organizations.test_org_api import OrganizationApiTests
from .organizations.test_org_mock import OrganizationMockTests
from .organizations.test_org_unittest import OrganizationUnitTests

from .stack.test_stacks import StacksTests

from .test_contentstack import ContentstackTests


def all_tests():
    test_module_contentstack = TestLoader().loadTestsFromTestCase(ContentstackTests)
    test_module_org_api = TestLoader().loadTestsFromTestCase(OrganizationApiTests)
    test_module_org_mock = TestLoader().loadTestsFromTestCase(OrganizationMockTests)
    test_module_org_unit = TestLoader().loadTestsFromTestCase(OrganizationUnitTests)
    test_module_user = TestLoader().loadTestsFromTestCase(UserApiTests)
    test_module_stacks = TestLoader().loadTestsFromTestCase(StacksTests)
    TestSuite([
        test_module_contentstack,
        test_module_org_api,
        test_module_org_mock,
        test_module_org_unit,
        test_module_user,
        test_module_stacks
    ])
