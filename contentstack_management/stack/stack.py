import json
from .._errors import ArgumentException
from ..aliases.aliases import Alias
from ..assets.assets import Assets
from ..branches.branches import Branch
from ..common import Parameter
from ..content_types.content_type import ContentType
from ..global_fields.global_fields import GlobalFields
from ..webhooks.webhook import Webhook
from ..workflows.workflows import Workflows
from ..metadata.metadata import Metadata
from ..roles.roles import Roles
from ..auditlogs.auditlog import Auditlog
from ..environments.environment import Environment
from ..locale.locale import Locale
from ..taxonomies.taxonomy import Taxonomy
from ..labels.label import Label
from ..bulk_operations.bulk_operation import BulkOperation
from ..releases.release import Releases
from ..delivery_token.delivery_token import DeliveryToken
from ..management_token.management_token import ManagementToken
from ..publish_queue.publish_queue import PublishQueue
from ..extensions.extension import Extension


class Stack(Parameter):
    """
    This class takes a base URL as an argument when it's initialized, 
    which is the endpoint for the RESTFUL API that
    we'll be interacting with. The create(), read(), update(), and delete() 
    methods each correspond to the CRUD 
    operations that can be performed on the API """

    def __init__(self, client, api_key=None):
        self.client = client
        if api_key is not None and not '':
            self.client.headers['api_key'] = api_key
        super().__init__(self.client)

    def fetch(self):
        """
        Fetches the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]

            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').fetch()
        -------------------------------
        """
        return self.client.get('stacks', headers=self.client.headers, params=self.params)

    def create(self, organization_uid, data):
        """
        Create the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>    "stack": {
            >>>         "name": "My New Stack",
            >>>         "description": "My new test stack",
            >>>         "master_locale": "en-us"
            >>>         }
            >>>      }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack().create('organization_uid', data).json()
        -------------------------------
        """
        if organization_uid is not None and '':
            self.client.headers['organization_uid'] = organization_uid
        data = json.dumps(data)
        return self.client.post('stacks', headers=self.client.headers,
                                params=self.params, data=data)

    def update(self, data):
        """
        Update the stacks entries 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]
            >>> data = {
            >>> "stack": {
            >>>     "name": "My New Stack",
            >>>     "description": "My new test stack",
            >>>     "master_locale": "en-us"
            >>>     }
            >>> }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').update(data).json()
        -------------------------------
        """
        data = json.dumps(data)
        return self.client.put('stacks', headers=self.client.headers, params=self.params, data=data)

    def delete(self):
        """
        Delete the stacks  
        :return: Json, with status code and message.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').delete()
        -------------------------------
        """
        return self.client.delete('stacks', headers=self.client.headers, params=self.params)

    def users(self):
        """
        Fetches the all users of a stack 
        :return: Json, with users of a stack details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            
            >>> result = client.stack().users()
        -------------------------------
        """
        return self.client.get('stacks/users', headers=self.client.headers, params=self.params)

    def update_user_role(self, data):
        """
        Update the user roles of the stacks 
        :return: Json, with user roles of stacks details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>     "users": {
            >>>         "user_uid": ["role_uid1", "role_uid2"]
            >>>       }
            >>>   }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='the_authtoken')
            >>> result = client.stack('api_key').update_user_role(data)
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.put('stacks/users/roles', headers=self.client.headers, params=self.params, data=data)

    def transfer_ownership(self, data):
        """
        Transfer owership of the stacks 
        :return: Json, with status code and message.
        -------------------------------
        [Example:]
            >>> data = {
                        "transfer_to": "manager@example.com"
                    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='the_authtoken')
            >>> result = client.stack('api_key').transfer_ownership(data)
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.post('stacks/transfer_ownership', headers=self.client.headers, data=data, params = self.params)

    def accept_ownership(self, user_id, ownership_token):
        """
        Accept ownership of the stack 
        :return: Json, with stacks details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='the_authtoken')
            >>> result = client.stack('api_key').accept_ownership('user_id', 'ownership_token')
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise PermissionError('api_key is required')
        if user_id is None or '':
            raise PermissionError('user_id is required')
        if ownership_token is None or '':
            raise PermissionError('ownership_token is required')
        url = f"stacks/accept_ownership/{ownership_token}"
        self.params.update({'api_key': self.client.headers['api_key'], 'uid': user_id})
        return self.client.get(url, headers=self.client.headers, params=self.params)

    def settings(self):
        """
        Fetches the stack settings 
        :return: Json, with stack settings details.
        -------------------------------
        [Example:]
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').settings()
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        return self.client.get('stacks/settings', headers=self.client.headers, params=self.params)

    def create_settings(self, data):
        """
        Create the stack settings 
        :return: Json, with stack setting details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>            "stack_settings": {
            >>>                "stack_variables": {
            >>>                    "enforce_unique_urls": 'true',
            >>>                    "sys_rte_allowed_tags": "style,figure,script",
            >>>                    "sys_rte_skip_format_on_paste": "GD:font-size"
            >>>               },
            >>>                "rte": {
            >>>                    "cs_only_breakline": 'true'
            >>>                }
            >>>            }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').create_stack_settings(data).json()

        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.post('stacks/settings', headers=self.client.headers, params=self.params, data=data)

    def reset_settings(self, data):
        """
        Reset the stack settings
        :return: Json, with stack setting details.
        -------------------------------
        [Example:]
            >>> data = {
            >>>       "stack_settings":{}
            >>>    }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').reset_stack_settings(data)
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.post('stacks/settings/reset', headers=self.client.headers, data=data, params = self.params)

    def share(self, data):
        """
        Share a stack to the users with user roles 
        :return: Json, with status code and message
        -------------------------------
        [Example:]
            >>> data = {
            >>>            "emails": [
            >>>                "*****"
            >>>            ],
            >>>            "roles": {
            >>>                "manager@example.com": [
            >>>                    "*******"
            >>>                ]
            >>>            }
            >>>        }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').share_stack(data).json()
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.post('stacks/share', headers=self.client.headers, params=self.params, data=data)



    def unshare(self, data):
        """
        Unshare a stack to the users with user roles 
        :return: Json, with status code and message
        -------------------------------
        [Example:]
            >>> data = {
            >>>     "email": "manager@example.com"
            >>>   }
            >>> import contentstack_management
            >>> client = contentstack_management.Client(authtoken='your_authtoken')
            >>> result = client.stack('api_key').unshare(data)
        -------------------------------
        """
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        data = json.dumps(data)
        return self.client.post('stacks/unshare', headers=self.client.headers, params=self.params, data=data)

    def global_fields(self, global_field_uid=None):
        if 'api_key' not in self.client.headers:
            raise Exception('api_key is required')
        return GlobalFields(self.client, global_field_uid)

    def branch(self, branch_uid=None):
        return Branch(self.client, branch_uid)

    def alias(self, alias_uid=None):
        return Alias(self.client, alias_uid)

    def content_types(self, content_type_uid=None, branch=None):
        return ContentType(self.client, content_type_uid, branch)

    def webhooks(self, webhook_uid=None):
        return Webhook(self.client, webhook_uid)

    def assets(self, asset_uid=None, branch=None):
        return Assets(self.client, asset_uid, branch)
    
    def workflows(self, workflow_uid=None):
        return Workflows(self.client, workflow_uid)
    
    def metadata(self, metadata_uid: str = None):
            return Metadata(self.client, metadata_uid)
    
    def roles(self, roles_uid: str = None):
            return Roles(self.client, roles_uid)
    
    def auditlog(self, log_item_uid: str = None):
            return Auditlog(self.client, log_item_uid)
    
    def environments(self, environment_name: str = None):
            return Environment(self.client, environment_name)
    
    def locale(self, locale_code: str = None):
            return Locale(self.client, locale_code)
    
    def taxonomy(self, taxonomy_uid: str = None):
            return Taxonomy(self.client, taxonomy_uid)
    
    def label(self, label_uid: str = None):
            return Label(self.client, label_uid)
    
    def bulk_operation(self):
            return BulkOperation(self.client)
    
    def releases(self, release_uid: str = None):
            return Releases(self.client, release_uid)

    def delivery_token(self, delivery_token: str = None):
            return DeliveryToken(self.client, delivery_token)

    def management_token(self, management_token: str = None):
            return ManagementToken(self.client, management_token)  
    
    def publish_queue(self, publish_queue_uid: str = None):
            return PublishQueue(self.client, publish_queue_uid)  
    
    def extension(self, extension_uid: str = None):
            return Extension(self.client, extension_uid) 