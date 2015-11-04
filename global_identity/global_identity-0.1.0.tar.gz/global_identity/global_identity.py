import requests
import json
import hmac
import hashlib


class GlobalIdentity:

    GLOBAL_IDENTITY_SERVER = 'dlpgi.dlp-payments.com'

    def __init__(self, app_key):
        self.app_key = app_key

    def validate_application(self, client_app_key, client_secret_key, resources):
        request = {}
        request['ApplicationKey'] = self.app_key
        request['ClientApplicationKey'] = client_app_key
        request['RawData'] = resources
        request['EncryptedData'] = hmac.new(client_secret_key, resources, hashlib.sha512).hexdigest()
        response = requests.post(
            'https://' + GlobalIdentity.GLOBAL_IDENTITY_SERVER +
            '/api/Authorization/ValidateApplication',
            data=request)
        return json.loads(response.text)

    def authenticate_user(self, username, password):
        request = {}
        request['ApplicationKey'] = self.app_key
        request['Email'] = username
        request['Password'] = password

        response = requests.post(
            'https://' + GlobalIdentity.GLOBAL_IDENTITY_SERVER +
            '/api/Authorization/Authenticate',
            data=request)
        return json.loads(response.text)

    def validate_token(self, token):
        request = {}
        request['ApplicationKey'] = self.app_key
        request['Token'] = token

        response = requests.post(
            'https://' + GlobalIdentity.GLOBAL_IDENTITY_SERVER +
            '/api/Authorization/ValidateToken',
            data=request)
        return json.loads(response.text)

    def is_user_in_role(self, user_key, roles):
        request = {}
        request['ApplicationKey'] = self.app_key
        request['UserKey'] = user_key
        request['RoleCollection'] = [y for x in [roles] for y in x]

        response = requests.post(
            'https://' + GlobalIdentity.GLOBAL_IDENTITY_SERVER +
            '/api/Authorization/IsUserInRole',
            data=request)
        return json.loads(response.text)
