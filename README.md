[![Contentstack](https://www.contentstack.com/docs/static/images/contentstack.png)](https://www.contentstack.com/)

## Contentstack Management Python SDK

Contentstack is a headless CMS with an API-first approach. It is a CMS that developers can use to build powerful cross-platform applications in their favorite languages. All you have to do is build your application frontend, and Contentstack will take care of the rest. [Read More](https://www.contentstack.com/).

This SDK uses the [Content Management API](https://www.contentstack.com/docs/developers/apis/content-management-api/) (CMA). The CMA is used to manage the content of your Contentstack account. This includes creating, updating, deleting, and fetching content of your account. To use the CMA, you will need to authenticate your users with a [Management Token](https://www.contentstack.com/docs/developers/create-tokens/about-management-tokens) or an [Authtoken](https://www.contentstack.com/docs/developers/apis/content-management-api/#how-to-get-authtoken). Read more about it in [Authentication](https://www.contentstack.com/docs/developers/apis/content-management-api/#authentication).

Note: By using CMA, you can execute GET requests for fetching content. However, we strongly recommend that you always use the [Content Delivery API](https://www.contentstack.com/docs/developers/apis/content-delivery-api/) to deliver content to your web or mobile properties.

### Prerequisite

You will need python 3 installed on your machine. You can install it
from [here](https://www.python.org/ftp/python/3.7.4/python-3.7.4-macosx10.9.pkg).

### Installation
#### Install contentstack pip

```python
pip install contentstack_management
```
To import the SDK, use the following command:
```python
import contentstack_management

client = contentstack_management.Client(authtoken='your_authtoken')
```

### Authentication
To use this SDK, you need to authenticate your users by using the Authtoken, credentials, or Management Token (stack-level token).
### Authtoken

An **Authtoken** is a read-write token used to make authorized CMA requests, and it is a **user-specific** token.
```python
client = contentstack_management.Client(authtoken= 'your_authtoken')
```
### Login
To Login to Contentstack by using credentials, you can use the following lines of code:
```python
client.login(email="email", password="password")

```

### Management Token
**Management Tokens** are **stack-level** tokens, with no users attached to them.

```python
result = client.stack(api_key = 'api_key', management_token= 'management_token' ).content_type('content_type_uid')
.fetch().json()
print(result)
```
### Contentstack Management Python SDK: 5-minute Quickstart
#### Initializing Your SDK:
To use the Python CMA SDK, you need to first initialize it. To do this, use the following code:

```python
import contentstack_management

client = contentstack_management.Client(authtoken= 'your_authtoken')
```
#### Fetch Stack Detail
Use the following lines of code to fetch your stack detail using this SDK:
```python
result = client.stack(api_key= 'api_key').fetch().json()
print(result)
```

#### Create Entry
To create an entry in a specific content type of a stack, use the following lines of code:

```python
entry  = {
  title: 'Sample Entry',
  url: '/sampleEntry'
}

result = client.stack(api_key= 'api_key').content_types('content_type_uid').entry().create(entry)
print(result.json())
```

#### Create Asset
The following lines of code can be used to upload assets to your stack:

```python
asset  = {
   upload: 'path/to/file',
   title: 'Asset Title'
}
asset = client().stack(api_key='api_key').assets()
result = asset.upload(asset)
```

### Helpful Links

-   [Contentstack Website](https://www.contentstack.com/)
-   [Official Documentation](https://contentstack.com/docs)
-   [Content Management API Docs](https://www.contentstack.com/docs/developers/apis/content-management-api)

### The MIT License (MIT)
Copyright © 2012-2023  [Contentstack](https://www.contentstack.com/). All Rights Reserved

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
