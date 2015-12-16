import urllib2
import json
import os
import base64

from oneid import keychain, service, utils

API_ENDPOINT = 'http://developer-portal.oneid.com/api'
PROJECT_ENDPOINT = '/projects/{project_id}'
SERVER_ENDPOINT = API_ENDPOINT + PROJECT_ENDPOINT + '/servers'
EDGE_DEVICE_ENDPOINT = API_ENDPOINT + PROJECT_ENDPOINT + '/edge_devices'


class CLISession(object):
    """
    Manage the active user's configuration and credentials

    :param project_name: Optional project name for settings
        specific to a project
    """
    def __init__(self, project_id=None):
        self._project_id = project_id
        self._encryption_key = None
        self._token = None

    @property
    def project(self):
        return self._project_id

    @project.setter
    def project(self, value):
        self._project_id = value

    @property
    def encryption_key(self):
        if self._encryption_key is None and self._project_id:
            self._load_project_settings()

        return self._encryption_key

    def _load_project_settings(self):
        """
        Given a project id, load settings
        :return:
        """
        with open(os.path.join(self.oneid_config_path(), 'credentials'), 'r') as credential_file:
            credentials = json.load(credential_file)
            if self._project_id and credentials.get(self._project_id):
                project_credentials = credentials.get(self._project_id)
            else:
                project_credentials = credentials.get('DEFAULT')

        if project_credentials is None:
            raise ValueError('Could not find any valid credentials for %s project' % self._project_id)

        der = base64.b64decode(project_credentials['SECRET'])
        self._token = keychain.Token.from_secret_der(der)
        self._token.identity = project_credentials.get('ID')
        self._encryption_key = base64.b64decode(project_credentials['AES'])

    def get_token(self):
        """
        Get the oneID Token associated with the current user and project

        :return: oneid.keychain.Token
        """
        if self._token is None and self._project_id:
            self._load_project_settings()

        return self._token

    def make_api_call(self, endpoint, http_method, **kwargs):
        """
        Make an API HTTP request to oneID

        :param endpoint: URL (all http methods are POST)
        :param kwargs: HTTP method is json, kwargs will be converted to json body
        :return: Response of request
        :raises TypeError: If the kwargs are None, json dumps will fail
        """
        if not self.get_token():
            raise ValueError('Please run: oneid-cli configure')

        http_request = urllib2.Request(endpoint)
        http_request.add_header('Content-Type', 'application/jwt')

        body_jwt = service.make_jwt(kwargs, self._token)

        auth_header_jwt = service.make_jwt({'nonce': utils.make_nonce(),
                                            'iss': self._token.identity},
                                           self._token)

        http_request.add_header('Authorization', 'Bearer %s' % auth_header_jwt)

        return urllib2.urlopen(http_request, body_jwt)

    def oneid_config_path(self):
        """
        Find the configuration path where the credentials and configuration
        files are stored

        :return: path to user's oneID CLI configuration
        """
        user_directory = os.path.expanduser('~')
        oneid_directory = '.oneid'
        return os.path.join(user_directory, oneid_directory)
