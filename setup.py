from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="contentstack-management",
    version="0.0.1",
    packages=find_packages(exclude=['tests']),
    py_modules=['_api_client', 'contentstack','common','_errors','_constant'],
    description="Contentstack API Client Library for Python",
    # package_dir={"": "contentstack"},
    # packages=find_namespace_packages(include=['contentstack_management.*']),
    # packages=find_packages(where="contentstack"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-management-python",
    author="Sunil",
    author_email="sunil.lakshman@contentstack.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.9", "requests >= 2.5.4"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2", "dotenv>=0.0.5"],
    },
    python_requires=">=3.9",
)
