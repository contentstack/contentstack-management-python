import os
import re
import sys
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

package = 'contentstack_management'

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)

def get_author_name(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__author__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_author_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__email__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)

setup(
    name="contentstack-management",
    version=get_version(package),
    packages=find_packages(exclude=['tests']),
    py_modules=['_api_client', 'contentstack','common','_errors','_constant'],
    description="Contentstack API Client Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-management-python",
    author=get_author_name(package),
    author_email=get_author_email(package),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.9", "requests >= 2.5.4", "requests-toolbelt >= 0.3.1"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2", "dotenv>=0.0.5"],
    },
    python_requires=">=3.9",
)
