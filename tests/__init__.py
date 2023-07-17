# pytest --html=tests/report/test-report.html 
# above command runs tests and test reports generates in tests/report location.
# nosetests --with-coverage --cover-html
# clean all the .pyc files
# find . -name \*.pyc -delete
# nosetests --with-coverage --cover-html
# pytest --cov=contentstack
# pytest -v --cov=contentstack --cov-report=html
# pytest --html=tests/report/test-report.html
from unittest import TestLoader, TestSuite

from .api.aliases.test_alias import AliaseApiTests
from .api.branches.test_branch_api import BranchApiTests
from .api.content_types.test_content_type_api import ContentTypeApiTests
from .api.organizations.test_org_api import OrganizationApiTests
from .api.stack.test_stack_apitest import StacksAPITests
from .api.users.test_api import UserApiTests
from .mock.branches.test_branch_mock import BranchMockTests
from .mock.organizations.test_org_mock import OrganizationMockTests
from .mock.users.test_mock import UserMockTests
from .test_contentstack import ContentstackTests
from .unit.aliases.test_alias import AliasesUnitTests
from .unit.branches.test_branch import BranchesUnitTests
from .unit.content_types.test_content_type import ContentTypeUnitTests
from .unit.organizations.test_organizations import OrganizationUnitTests
from .unit.stack.test_stack import StacksUnitTests
from .unit.users.test_users import UserUnitTests
from .unit.entry.test_entry import EntryUnitTests


def all_tests():
    test_module_contentstack = TestLoader().loadTestsFromTestCase(ContentstackTests)

    test_module_org_unit = TestLoader().loadTestsFromTestCase(OrganizationUnitTests)
    test_module_user_unittest = TestLoader().loadTestsFromTestCase(UserUnitTests)
    test_module_stacks_unit = TestLoader().loadTestsFromTestCase(StacksUnitTests)
    test_module_org_api = TestLoader().loadTestsFromTestCase(OrganizationApiTests)
    test_module_stacks_api = TestLoader().loadTestsFromTestCase(StacksAPITests)
    test_module_user_api = TestLoader().loadTestsFromTestCase(UserApiTests)
    test_module_org_mock = TestLoader().loadTestsFromTestCase(OrganizationMockTests)
    test_module_user_mock = TestLoader().loadTestsFromTestCase(UserMockTests)
    test_module_entry_unittest = TestLoader().loadTestsFromTestCase(EntryUnitTests)


    TestSuite([
        test_module_contentstack,
        test_module_org_api,
        test_module_org_mock,
        test_module_org_unit,
        test_module_user_api,
        test_module_user_mock,
        test_module_user_unittest,
        test_module_stacks_api,
        test_module_stacks_unit,
        test_module_entry_unittest

    ])
