from __future__ import absolute_import
import base64
import urllib3

# Default Base url
host = "https://localhost/"

# Default api client
api_client = None

# Authentication settings

api_key = {}
api_key_prefix = {}
username = ''
password = ''

auth_token = ''

def get_api_key_with_prefix(key):
    global api_key
    global api_key_prefix

    if api_key.get(key) and api_key_prefix.get(key):
      return api_key_prefix[key] + ' ' + api_key[key]
    elif api_key.get(key):
      return api_key[key]

def get_basic_auth_token():
    global username
    global password

    return urllib3.util.make_headers(basic_auth=username + ':' + password).get('authorization')

def auth_settings():
    return { 
                'oauth2': {
                    'type': 'oauth2',
                    'in': 'header',
                    'key': 'Authorization',
                    'value': 'Bearer ' + auth_token
                },
             
           }
