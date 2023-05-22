"""The __init__.py file that contains modules that need to import"""


from .core.login import Login
from .core.error import Error

from contentstack_management import contentstack

__title__ = 'contentstack-cms'
__author__ = 'contentstack'
__status__ = 'debug'
__version__ = '0.0.1'
__host__ = 'api.contentstack.io'
__protocol__ = 'https://'
__api_version__ = 'v3'
__endpoint__ = 'https://api.contentstack.io/v3/'
__email__ = 'mobile@contentstack.com'
__issues__ = 'customer_care@contentstack.com'
