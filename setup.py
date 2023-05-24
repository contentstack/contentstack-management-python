from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="contentstack-management",
    version="0.0.2",
    packages=['contentstack_management'],
    description="Contentstack API Client Library for Python",
    # package_dir={"": "contentstack"},
    # packages=find_packages(where="contentstack"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-management-python",
    author="Sunil",
    author_email="sunil,lakshman@contentstack.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
