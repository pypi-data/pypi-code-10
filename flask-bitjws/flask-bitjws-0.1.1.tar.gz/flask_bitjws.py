"""
The FlaskBitjws source code. Everything fits in this file, for now.
"""
import bitjws
import time
import copy
import urlparse
from flask import Response, current_app
from flask.ext import login


class FlaskUser(login.UserMixin):
    """
    A flask_login UserMixin.
    """

    def __init__(self, username, salt):
        super(FlaskUser, self).__init__()
        self.salt = salt
        self.username = username


def load_user_from_request(req):
    """
    Just like the Flask.login load_user_from_request

    This function performs almost entirely bitjws authentication tasks.
    If you need to customize the user loading from your database,
    the FlaskBitjws.get_user_by_key method is the one to modify.

    :param req: The flask request to load a user based on.
    """
    if "application/jose" in req.headers['content-type']:
        path = urlparse.urlsplit(req.url).path
        for rule in current_app.url_map.iter_rules():
            if path == rule.rule and req.method in rule.methods:
                dedata = req.get_data().decode('utf8')
                req.jws_header, req.jws_payload = \
                    bitjws.validate_deserialize(dedata, requrl=rule.rule)
                break
    if not hasattr(req, 'jws_header') or req.jws_header is None:
        return None

    if (not 'iat' in req.jws_payload or
            req.jws_payload['iat'] <=
            current_app.bitjws.get_last_nonce(req.jws_header['kid'],
                                              req.jws_payload['iat'])):
        return None
    rawu = current_app.bitjws.get_user_by_key(req.jws_header['kid'])
    user = FlaskUser(**rawu)
    return user


class FlaskBitjws(object):
    """
    A wrapper class for the main Flask bitjws application.
    Performs bitjws authentication checks and signs responses.

    Overwrite the methods with real DB calls:

    get_last_nonce
    get_user_by_key
    """

    def __init__(self, app, privkey=None,
                 loginmanager=None):
        """
        Initialize a flask-bitjws Application with optional LoginManager.
        If you do not provide your own LoginManager one will be created.

        Create or set the private key to use with this application.

        :param str app: The flask application
        :param str privkey: the bitjws private key to use for signing responses
        :param flask.ext.login.LoginManager loginmanager: An optional LoginManager
        """
        if privkey is not None and isinstance(privkey, str):
            self._privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))
        elif privkey is not None and isinstance(privkey, bitjws.PrivateKey):
            self._privkey = privkey
        else:
            self._privkey = bitjws.PrivateKey()
        self.pubkey = bitjws.pubkey_to_addr(self._privkey.pubkey.serialize())
        print "Initializing FlaskBitjws from with address: {}".format(self.pubkey)

        if loginmanager is None:
            loginmanager = login.LoginManager()
            loginmanager.anonymous_user = login.AnonymousUserMixin
            loginmanager.init_app(app)
        loginmanager.request_loader(load_user_from_request)
        app.bitjws = self

    def create_response(self, payload):
        """
        Create a signed bitjws response using the supplied payload.
        The response content-type will be 'application/jose'.

        :param payload: The response content. Must be json-serializable.
        :return: The signed Response with headers.
        :rtype: flask.Response
        """
        signedmess = bitjws.sign_serialize(self._privkey, requrl='/response',
                                           iat=time.time(), data=payload)
        return Response(signedmess, mimetype='application/jose')

    ##############################################################
    # DB STUBS Section
    # Overwrite the remaining methods in this class for your own.
    ##############################################################
    def get_last_nonce(self, key, nonce):
        """
        This method is only an example! Replace it with a real nonce database.

        :param str key: the public key the nonce belongs to
        :param int nonce: the latest nonce
        """
        if not hasattr(self, '_example_nonce_db'):
            # store nonces as a pair {key: lastnonce}
            self._example_nonce_db = {}
        if not key in self._example_nonce_db:
            self._example_nonce_db[key] = nonce
            return 0
        else:
            oldnonce = copy.copy(self._example_nonce_db[key])
            self._example_nonce_db[key] = nonce
            return oldnonce

    def get_user_by_key(self, key):
        """
        This method is only an example! Replace it with a real user database.

        :param str key: the public key the user belongs to
        """
        if not hasattr(self, '_example_user_db'):
            self._example_user_db = {}

        if key in self._example_user_db:
            return self._example_user_db[key]
        return None

