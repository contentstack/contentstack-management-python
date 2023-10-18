"""
Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded in your Contentstack repository for future use. This class takes a base URL as an argument when it's initialized, 
which is the endpoint for the RESTFUL API that we'll be interacting with.
The create(), read(), update(), and delete() methods each correspond to 
the CRUD operations that can be performed on the API
"""
import json
from ..common import Parameter

class Assets(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, asset_uid, branch):
        self.client = client
        self.asset_uid = asset_uid
        self.branch = branch
        self.api_key = self.client.headers['api_key']
        super().__init__(self.client)

    def find(self):
        """
        The Get all assets request returns comprehensive information on all assets available in a stack.

        :return: The code is returning the result of an API call made using the `get` method of the
        `api_client` object. The URL being used for the API call is "assets". The headers and parameters
        for the API call are being passed as arguments to the `get` method. The result of the API call
        is being returned.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.find()
        --------------------------------
        """

        url = "assets"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def fetch(self):
        """
        The Get an asset request returns comprehensive information about a specific version of an asset of a stack.

        :return: The fetch method returns the response from the Get an asset request, which contains
        comprehensive information about a specific version of an asset of a stack.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.fetch("asset_uid")
        --------------------------------
        """

        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def delete(self):
        """
        The Delete asset call will delete an existing asset from the stack.

        :return: The delete() method returns the status code and message as a response.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.delete("asset_uid")
        --------------------------------
        """

        url = F"assets/{self.asset_uid}"
        return self.client.delete(url, headers = self.client.headers, params = self.params)

    def specific_folder(self, folder_uid):
        """
        The Get assets of a specific folder retrieves all assets of a specific asset folder; 
        however, it doesn't retrieve the details of subfolders within it.

        :param folder_uid: The folder_uid parameter is the unique identifier of the specific asset
        folder you want to retrieve assets from
        :return: the response from the API call made to retrieve all assets of a specific asset folder.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.specific_folder("folder_uid")
        --------------------------------
        """

        url = "assets"
        Parameter.add_param(self, "folder", folder_uid)
        return self.client.get(url , headers = self.client.headers, params = self.params)

    def subfolders(self, folder_uid):
        r"""
        The Get assets and folders of a parent folder retrieves details of both assets and 
        asset subfolders within a specific parent asset folder.

        :param folder_uid: The `folder_uid` parameter is the unique identifier of the parent asset
        folder for which you want to retrieve the details of assets and subfolders
        :return: the response from the API call made to retrieve information about assets and subfolders
        within a specific parent asset folder.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.subfolders("folder_uid")
        --------------------------------
        """

        url = "assets"
        Parameter.add_param(self, "include_folders", True)
        Parameter.add_param(self, "folder", folder_uid)
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def upload(self, file_path):
        """
        The Upload asset request uploads an asset file to your stack.

        :param file_path: The `file_path` parameter is the path to the file that you want to upload. It
        should be a string representing the file's location on your local machine
        :return: the result of a POST request to the "assets" endpoint with the specified parameters and
        file.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> file_path = ""
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.upload(file_path)
        --------------------------------
        """

        url = "assets"
        Parameter.add_header(self, "Content-Type", "multipart/form-data")
        files = {"asset": open(f"{file_path}",'rb')}
        return self.client.post(url, headers = self.client.headers, params = self.params, files = files)
    
    def replace(self, file_path):
        """
        The Replace asset call will replace an existing asset with another file on the stack.
        
        :param file_path: The `file_path` parameter is the path to the file that you want to replace the
        existing asset with. It should be a string representing the file path on your local machine
        :return: The code is returning the result of a PUT request made to the specified URL with the
        provided headers, parameters, and files.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> file_path = ""
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.replace(file_path)
        --------------------------------
        """

        url = f"assets/{self.asset_uid}"
        Parameter.add_header(self, "Content-Type", "multipart/form-data")
        files = {"asset": open(f"{file_path}",'rb')}
        return self.client.put(url, headers = self.client.headers, params = self.params, files = files)
    
    def generate(self, data):
        """
        The Generate Permanent Asset URL request allows you to generate a permanent URL for an asset. 
        This URL remains constant irrespective of any subsequent updates to the asset.
        
        :param data: The `data` parameter is a dictionary that contains the data to be sent in the
        request body. It will be converted to a JSON string using the `json.dumps()` function before
        being sent
        :return: The code is returning the result of the `put` request made to the specified URL with
        the provided headers, parameters, and data.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
            >>>    "asset": {
            >>>        "permanent_url": "https://images.contentstack.io/v3/assets/stack_api_key/asset_UID/sample-slug.jpeg"
            >>>        }
            >>>    } 
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.generate(data)
        --------------------------------
        """

        data = json.dumps(data)
        url = f"assets/{self.asset_uid}"
        return self.client.put(url, headers = self.client.headers, params = self.params, data = data)

    def download(self):
        """
        The Download an asset with permanent URL request displays an asset in the response. 
        The asset returned in the response can be saved to your local storage system. Make sure to specify the unique identifier (slug) in the request URL.

        :return: The code is returning the result of the `get` request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.download()
        --------------------------------
        """
        
        url = f"assets/{self.api_key}/{self.asset_uid}"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def rte(self):
        """
        The Get information on RTE assets call returns comprehensive information on all assets uploaded through the Rich Text Editor field.
        
        :return: the result of a GET request to the specified URL with the provided headers and
        parameters.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.rte()
        --------------------------------
        """

        url = "assets/rt"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def version_naming(self, version_number, data):
        """
        The Set Version Name for Asset request allows you to assign a name to a specific version of an asset.

        :param data: The `data` parameter is a JSON object that contains the information you want to
        update for the specified version
        :param version_number: The `version_number` parameter is the number or identifier of the version
        that you want to update the name for
        :return: the result of the PUT request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> version_number = 1
            >>> data = {
	        >>>     "upload": {
		    >>>     "_version_name": "Version name"
	        >>>     }
            >>> }
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.version_naming(version_number, data)
        --------------------------------
        """
        
        data = json.dumps(data)
        url = f"assets/{self.asset_uid}/versions/{version_number}/name"
        return self.client.post(url, headers = self.client.headers, params = self.params, data = data)
    
    def version(self):
        """
        The Get Details of All Versions of an Asset request allows you to retrieve the details of all the versions of an asset.
        
        :return: The code is returning the result of the `client.get` method call.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.version()
        --------------------------------
        """

        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}/versions"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def version_delete(self, version_number):
        """
        The Delete Version Name of Asset request allows you to delete the name assigned to a specific version of an asset. This request resets the name of the asset version to the version number.

        :param version_number: The version number of the asset that you want to delete
        :return: the result of the delete request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> version_number = 1
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.version_delete(version_number)
        --------------------------------
        """
        
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        if version_number is None:
            raise Exception('Version Number is required')
        url = f"assets/{self.asset_uid}/versions/{version_number}/name"
        return self.client.delete(url, headers = self.client.headers, params = self.params)

    def references(self):
        """
        The Get asset references request returns the details of the entries and the content types in which the specified asset is referenced.

        :return: the result of a GET request to a specific URL, with headers and parameters included.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.references()
        --------------------------------
        """
        
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}/references"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def specific_asset_type(self, asset_type):
        """
        The Get either only images or videos request retrieves assets that are either image or video files, based on query request.

        :return: the result of a GET request to a specific URL, with headers and parameters included.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset_type = "images"
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.specific_asset_type(asset_type)
        --------------------------------
        """
        
        if asset_type is None or '':
            raise Exception('asset_type is required')
        url = f"assets/{asset_type}"
        return self.client.get(url, headers = self.client.headers, params = self.params)

    def update_asset_revision(self, data):
        """
        The Update asset revision call upgrades a specified version of an asset as the latest version of that asset.
        
        :param data: The `data` parameter is a dictionary that contains the updated information for the
        asset revision. It will be converted to a JSON string using the `json.dumps()` function before
        sending the request
        :return: the result of the `put` request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "title": "Title",
		    >>>         "description": "Description"
	        >>>     },
	        >>>     "version": 2
            >>> }
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.update_asset_revision(data)
        --------------------------------
        """
        
        data = json.dumps(data)
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}"
        return self.client.put(url, headers = self.client.headers, params = self.params, data = data)

    def update(self, data):
        """
        The Update asset request allows you to update the title and description of an asset.

        :param data: The `data` parameter is a dictionary that contains the updated information for the
        asset revision. It will be converted to a JSON string using the `json.dumps()` function before
        being sent in the request
        :return: the result of the `self.client.put()` method call.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "title": "Title"
	        >>>     }
            >>> }
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.update(data)
        --------------------------------
        """

        data = json.dumps(data)
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}"
        Parameter.add_header(self, "Content-Type", "multipart/form-data")
        return self.client.put(url, headers = self.client.headers, params = self.params, data = data)

    def publish(self, data):
        """
        The Publish an asset call is used to publish a specific version of an asset on the desired environment either immediately or at a later date/time.

        :param data: The `data` parameter is the data that you want to publish. It should be in JSON
        format
        :return: the result of the `client.post` method call.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "locales": [
			>>>             "en-us"
		    >>>         ],
		    >>>         "environments": [
			>>>             "development"
		    >>>         ]
	        >>>     },
	        >>>     "version": 1,
	        >>>     "scheduled_at": "2019-02-08T18:30:00.000Z"
            >>> }
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.publish(data)
        --------------------------------
        """
        
        data = json.dumps(data)
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}/publish"
        return self.client.post(url, headers = self.client.headers, data = data)
    
    def unpublish(self, data):
        """
        The Unpublish an asset call is used to unpublish a specific version of an asset from a desired environment.

        :param data: The `data` parameter is a JSON object that contains the necessary information for
        the unpublish operation. It is being converted to a JSON string using the `json.dumps()`
        function before being sent in the request
        :return: the result of the `post` request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "locales": [
			>>>             "en-us"
		    >>>         ],
		    >>>         "environments": [
			>>>             "development"
		    >>>         ]
	        >>>     },
	        >>>     "version": 1,
	        >>>     "scheduled_at": "2019-02-08T18:30:00.000Z"
            >>> }
            >>> asset = client().stack(api_key='api_key').assets(asset_uid='asset_uid')
            >>> response = asset.unpublish(data)
        --------------------------------
        """

        data = json.dumps(data)
        if self.asset_uid is None or '':
            raise Exception('asset_uid is required')
        url = f"assets/{self.asset_uid}/unpublish"
        return self.client.post(url, headers = self.client.headers, data = data)
    
    def folder(self, folder_uid):
        """
        The Get a single folder call gets the comprehensive details of a specific asset folder by means of folder UID.

        :param folder_uid: The `folder_uid` parameter is the unique identifier of the folder that you
        want to retrieve from the server
        :return: the result of a GET request to the specified URL, using the provided parameters and
        headers.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.folder_collection(folder_uid='folder_uid')
        --------------------------------
        """

        url = f"assets/folders/{folder_uid}"
        return self.client.get(url, params = self.params, headers = self.client.headers)

    def folder_by_name(self):
        """
        The Get a single folder by name call retrieves a specific asset folder based on the name provided.

        :param query: The "query" parameter is a string that represents the search query for the folder
        collection. It is used to filter the results and retrieve only the folders that match the
        specified query
        :return: the result of the GET request made by the `self.client.get()` method.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> query = {"is_dir": True, "name": "folder_name"}
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.folder_collection(query)
        --------------------------------
        """

        url = "assets"
        query = {"is_dir": True, "name": "folder_name"}
        Parameter.add_param(self, "query", query)
        return self.client.get(url, params = self.params, headers = self.client.headers)

    def get_subfolders(self, folder_uid):
        """
        The Get subfolders of a parent folder request retrieves the details of only the subfolders of a specific asset folder. This request does not retrieve asset files.
        
        :param folder_uid: The folder_uid parameter is used to specify the unique identifier of the
        folder you want to include in the query
        :param query: The "query" parameter is used to specify a search query for filtering the results.
        It allows you to search for specific items within the folder
        :return: the result of a GET request made by the client.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> query = {"is_dir": True}
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.folder_collection(folder_uid='folder_uid', query)
        --------------------------------
        """

        url = "assets"
        query = {"is_dir": True}
        Parameter.add_param(self, "include_folders", True)
        Parameter.add_param(self, "query",query)
        Parameter.add_param(self, "folder", folder_uid)
        return self.client.get(url, params = self.params, headers = self.client.headers)

    def create_folder(self, data):
        """
        The Create a folder call is used to create an asset folder and/or add a parent folder to it (if required).
        
        :param data: The `data` parameter is the payload or body of the HTTP request. It contains the
        data that you want to send to the server when creating a folder. The specific format and
        structure of the data will depend on the API you are using. You should consult the API
        documentation to determine the required format
        :return: the result of the `self.client.post()` method.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "name": "Demo"
	        >>>     }
            >>> }
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.create_folder(data)
        --------------------------------
        """
        
        url = "assets/folders"
        return self.client.post(url, params = self.params, headers = self.client.headers, data = data)

    def update_or_move(self, folder_uid, data):
        """
        The Update or move folder request can be used either to update the details of a folder or set the parent folder if you want to move a folder under another folder.
        
        :param folder_uid: The `folder_uid` parameter is the unique identifier of the folder that you
        want to update
        :param data: The `data` parameter is a dictionary that contains the updated information for the
        folder. It will be converted to a JSON string using the `json.dumps()` function before sending
        it to the server
        :return: the result of the `self.client.put()` method call.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> data = {
	        >>>     "asset": {
		    >>>         "name": "Demo"
	        >>>     }
            >>> }
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.update_or_move(folder_uid='folder_uid', data)
        --------------------------------
        """

        data = json.dumps(data)
        url = f"assets/folders/{folder_uid}"
        return self.client.put(url, params = self.params, headers = self.client.headers, data = data)

    def delete_folder(self, folder_uid):
        """
        The Delete a folder call is used to delete an asset folder along with all the assets within that folder.

        :param folder_uid: The `folder_uid` parameter is the unique identifier of the folder that you
        want to delete. It is used to specify which folder should be deleted
        :return: the result of the delete request made to the specified URL.
        --------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> asset = client().stack(api_key='api_key').assets()
            >>> response = asset.delete(folder_uid='folder_uid')
        --------------------------------
        """

        url = f"assets/folders/{folder_uid}"
        return self.client.delete(url,  headers = self.client.headers)
