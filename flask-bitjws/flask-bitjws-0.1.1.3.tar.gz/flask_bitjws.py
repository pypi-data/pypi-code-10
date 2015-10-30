"""
The FlaskBitjws source code. Everything fits in this file, for now.
"""
import bitjws
import time
import copy
import urlparse
from flask import Response, current_app
from flask.ext import login


"""
DB STUBS Section
Overwrite the functions in this section with your own.
"""
def get_last_nonce(app, key, nonce):
    """
    This method is only an example! Replace it with a real nonce database.

    :param str key: the public key the nonce belongs to
    :param int nonce: the latest nonce
    """
    if not hasattr(app, '_example_nonce_db'):
        # store nonces as a pair {key: lastnonce}
        app._example_nonce_db = {}
    if not key in app._example_nonce_db:
        app._example_nonce_db[key] = nonce
        return 0
    else:
        oldnonce = copy.copy(app._example_nonce_db[key])
        app._example_nonce_db[key] = nonce
        return oldnonce


def get_user_by_key(app, key):
    """
    This method is only an example! Replace it with a real user database.

    :param str key: the public key the user belongs to
    """
    if not hasattr(app, '_example_user_db'):
        app._example_user_db = {}

    if key in app._example_user_db:
        return app._example_user_db[key]
    return None
"""
DB STUBS Section End
"""


def load_jws_from_request(req):
    """
    This function performs almost entirely bitjws authentication tasks.
    If valid bitjws message and signature headers are found,
    then the request will be assigned 'jws_header' and 'jws_payload' attributes.

    :param req: The flask request to load the jwt claim set from.
    """
    jws_header = None
    jws_payload = None
    if "application/jose" in req.headers['content-type']:
        path = urlparse.urlsplit(req.url).path
        for rule in current_app.url_map.iter_rules():
            if path == rule.rule and req.method in rule.methods:
                dedata = req.get_data().decode('utf8')
                req.jws_header, req.jws_payload = \
                    bitjws.validate_deserialize(dedata, requrl=rule.rule)
                break


def load_user_from_request(req):
    """
    Just like the Flask.login load_user_from_request

    If you need to customize the user loading from your database,
    the FlaskBitjws.get_user_by_key method is the one to modify.

    :param req: The flask request to load a user based on.
    """
    load_jws_from_request(req)
    if not hasattr(req, 'jws_header') or req.jws_header is None or not \
            'iat' in req.jws_payload:
        return None

    ln = current_app.bitjws.get_last_nonce(current_app,
                                           req.jws_header['kid'],
                                           req.jws_payload['iat'])

    if (ln is None or 'iat' not in req.jws_payload or
            req.jws_payload['iat'] * 1000 <= ln):
        return None

    rawu = current_app.bitjws.get_user_by_key(current_app,
                                              req.jws_header['kid'])
    if rawu is None:
        return None
    return FlaskUser(rawu)

class FlaskUser(login.UserMixin):

    def __init__(self, dbuser):
        super(FlaskUser, self).__init__()
        self.dbuser = dbuser

    @property
    def id(self):
        return self.dbuser.id


class FlaskBitjws(object):
    """
    A wrapper class for the main Flask bitjws application.
    Performs bitjws authentication checks and signs responses.

    Overwrite the methods with real DB calls:

    get_last_nonce
    get_user_by_key
    """

    def __init__(self, app, privkey=None,
                 loginmanager=None,
                 get_last_nonce=get_last_nonce,
                 get_user_by_key=get_user_by_key):
        """
        Initialize a flask-bitjws Application with optional LoginManager.
        If you do not provide your own LoginManager one will be created.

        Create or set the private key to use with this application.

        :param str app: The flask application
        :param str privkey: the bitjws private key to use for signing responses
        :param flask.ext.login.LoginManager loginmanager: An optional LoginManager
        :param function get_last_nonce: A function to overwrite this class's stub. 
        :param function get_user_by_key: A function to overwrite this class's stub.
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

        self.get_last_nonce = get_last_nonce
        self.get_user_by_key = get_user_by_key
    
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

