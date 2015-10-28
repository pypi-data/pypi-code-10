import bitjws
from flask import Flask, Response, request


def get_bitjws_header_payload(req):
    """
    :param flask.Request request: The raw request with bitjws message body
    :return: the JWS header and payload, in that order
    """
    h, p = bitjws.validate_deserialize(req.get_data().decode('utf8'))
    if h is None:
        # Validation failed.
        return None, None
    return h, p


class Application(Flask):
    """
    A wrapper for the main Flask bitjws application.
    """

    def __init__(self, name, privkey=None, **kwargs):
        """
        Initialize a Flask-bitjws Application.

        :param str name: the application's name
        :param str privkey: the bitjws private key to use for signing responses
        """
        super(Application, self).__init__(name, **kwargs)
        self.before_request(self.__augment_request)
        if privkey is not None and isinstance(privkey, str):
            self._privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))
        elif privkey is not None and isinstance(privkey, bitjws.PrivateKey):
            self._privkey = privkey
        else:
            self._privkey = bitjws.PrivateKey()
        self.pubkey = bitjws.pubkey_to_addr(self._privkey.pubkey.serialize())
        print "Initializing server with address: {}".format(self.pubkey)


    def __augment_request(self):
        """
        If the request content-type is 'application/jose',
        extract the jws payload and header from the request body.
        """
        if "application/jose" in request.headers['content-type']:
            request.jws_header, request.jws_payload = \
                    get_bitjws_header_payload(request)


    def create_bitjws_response(self, payload):
        """
        Create a signed bitjws response using the supplied payload.
        The response content-type will be 'application/jose'.

        :param payload: The response content. Must be json-serializable.
        :return: The signed Response with headers.
        :rtype: flask.Response
        """
        signedmess = bitjws.sign_serialize(self._privkey, data=payload)
        return Response(signedmess, mimetype='application/jose')

