'''
Data models powering the library.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

import hashlib
import os

import bcrypt
from requests.compat import urlencode, urlunparse, quote, quote_plus

from .exceptions import InvalidUserKeyError
from .defaults import (
    VALID_DECODED_KEY_LENGTH, VALID_ENCODED_KEY_LENGTH,
    VALID_ENCODED_KEY_CHARACTERS)
from ._utils import toutf8

class Cluster(object):
    '''
    Store cluster connection parameters and provide connection data for cluster
    and its specific nodes.

    Initialization parameters:
      - name -- name of the cluster; used as a domain name to connect to the
        cluster in absence of ip_address
      - ip_address -- IP address of a node belonging to the cluster; if set,
        used to connect to the cluster instead of cluster name
      - is_secure -- flag determining whether the connection will be secured by
        SSL
      - port -- custom remote port to connect to; if unset, default ports will
        be used (443 for https, 80 for http)
    '''

    def __init__(self,
                 name,
                 ip_address=None,
                 is_secure=True,
                 port=None):
        self.name = toutf8(name)
        self.ip_address = toutf8(ip_address) if ip_address is not None else None
        self.is_secure = is_secure
        self.port = int(port) if port is not None else None

    @property
    def url(self):
        return self.get_host_url(self.host)

    def get_host_url(self, host):
        '''Get URL for a node host specified in the argument.'''
        data = (self.scheme, self.get_host_netloc(host), '', '', '', '')
        url = urlunparse(data)
        return url

    @property
    def host(self):
        return self.ip_address if self.ip_address else self.name

    @property
    def scheme(self):
        if self.is_secure:
            scheme = 'https'
        else:
            scheme = 'http'
        return scheme

    def get_host_netloc(self, host):
        '''
        Get network location (host + port) for a node host specified in the
        argument.
        '''
        if self.port is not None:
            netloc = ':'.join((host, str(self.port)))
        else:
            netloc = host
        return netloc


class QueryParameters(object):
    '''For a given API function, store its query parameters.'''

    def __init__(self,
                 sx_verb,
                 path_items=None,
                 bool_params=None,
                 dict_params=None):
        path_items = [] if path_items is None else path_items
        bool_params = set() if bool_params is None else bool_params
        dict_params = {} if dict_params is None else dict_params

        path_items = [toutf8(elt) for elt in path_items]
        bool_params = {toutf8(elt) for elt in bool_params}
        dict_params = {toutf8(key): toutf8(value)
                       for key, value in dict_params.iteritems()}

        self.sx_verb = sx_verb
        self.path_items = path_items
        self.bool_params = bool_params
        self.dict_params = dict_params

    @property
    def path(self):
        path = '/'.join(quote(item) for item in self.path_items)
        return path

    @property
    def params(self):
        items_to_join = {quote_plus(item) for item in self.bool_params}
        param_string = urlencode(self.dict_params)
        items_to_join.add(param_string)
        param_string = '&'.join(item for item in items_to_join if item)
        return param_string

    @property
    def verb(self):
        if self.sx_verb.startswith('JOB_'):
            verb = self.sx_verb.split('_', 1)[-1]
        else:
            verb = self.sx_verb
        return verb

    @property
    def is_complex(self):
        if self.sx_verb.startswith('JOB_'):
            is_complex = True
        else:
            is_complex = False
        return is_complex

    @property
    def sx_verb(self):
        return self._sx_verb

    @sx_verb.setter
    def sx_verb(self, value):
        self._sx_verb = value.upper()

    def __repr__(self):
        attr_string_pairs = ('%s=%r' % (key, getattr(self, key))
                 for key in dir(self)
                 if not key.startswith('_'))
        attr_string = ', '.join(attr_string_pairs)
        text_repr = '%s(%s)' % (self.__class__.__name__, attr_string)
        return text_repr


class UserData(object):
    '''
    Prepare user access data.

    In addition to the default initialization, the following class methods can
    be used to initialize the object:
      - from_key;
      - from_key_path;
      - from_userpass_pair.

    For example, to initialize the object based on username and password, run:
        UserData.from_userpass_pair(username, password, uuid)
    '''

    def __init__(self, dec_key):
        self._key = dec_key

    @property
    def key(self):
        return self._key

    @property
    def uid(self):
        return self._key[:20]

    @property
    def secret_key(self):
        return self._key[20:40]

    @property
    def padding(self):
        return self._key[40:42]

    @classmethod
    def from_key(cls, enc_key):
        '''Prepare user access data using base64-encoded user key.'''
        dec_key = cls._decode_key(enc_key)
        return cls(dec_key)

    @classmethod
    def from_key_path(cls, key_path):
        '''
        Prepare user access data using path to the file containing
        base64-encoded user key.
        '''
        key_path = os.path.expanduser(key_path)
        enc_key = cls._load_key(key_path)
        dec_key = cls._decode_key(enc_key)
        return cls(dec_key)

    @classmethod
    def from_userpass_pair(cls, username, password, cluster_uuid):
        '''
        Prepare user access data based on username, password and cluster UUID.

        Note that username and password should be encoded in UTF-8.
        '''
        username = toutf8(username)
        password = toutf8(password)

        # prepare uid
        sha1 = hashlib.sha1()
        sha1.update(username)
        uid = sha1.digest()

        # prepare salt for password hashing
        sha1 = hashlib.sha1()
        sha1.update(cluster_uuid)
        sha1.update(username)
        salt = sha1.digest()[:16]
        encsalt = bcrypt.encode_salt(salt, 12)

        # prepare hashed password with '2b' prefix
        hashpw = bcrypt.hashpw(password, encsalt)
        hashpw = '$2b' + hashpw[3:]

        # prepare secret key
        sha1 = hashlib.sha1()
        sha1.update(cluster_uuid)
        sha1.update(hashpw)
        secret = sha1.digest()

        padding = '\x00\x00'
        dec_key = ''.join([uid, secret, padding])
        return cls(dec_key)

    @staticmethod
    def _load_key(path):
        '''Read base64-encoded key from 'path'.'''
        with open(path, 'rb') as keyfile:
            enc_key = keyfile.read(VALID_ENCODED_KEY_LENGTH)
        return enc_key

    @staticmethod
    def _decode_key(enc_key):
        '''Verify and decode base64-encoded key.'''
        if len(enc_key) < VALID_ENCODED_KEY_LENGTH:
            raise InvalidUserKeyError('Invalid user key file length')

        # Python 2.7.10 documentation incorrectly states that
        # 'base64.b64decode' raises 'TypeError' in case of invalid input
        # characters. In reality, invalid input characters are silently
        # ignored. The issue has been reported in
        #   https://bugs.python.org/issue22088
        # Input validity is checked independently of 'base64.b64decode', below.
        invalid_char_in_key = any(char not in VALID_ENCODED_KEY_CHARACTERS
                                    for char in enc_key)
        if invalid_char_in_key:
            raise InvalidUserKeyError('Invalid character in user key file')

        dec_key = enc_key.decode('base64')
        if len(dec_key) != VALID_DECODED_KEY_LENGTH:
            raise InvalidUserKeyError('Invalid decoded user key length')
        return dec_key
