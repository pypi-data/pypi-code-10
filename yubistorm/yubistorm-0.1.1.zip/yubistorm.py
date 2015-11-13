"""Asynchronous client for YubiCloud and Tornado."""
import copy
import sys
import random
import base64
import uuid
import urllib.parse
from hashlib import sha1
import hmac
import tornado
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    raise Exception("YubiStorm requires at least Python version 3.5.")
if tornado.version < "4.3":
    raise Exception("YubiStorm requires at least tornado version 4.3.")

__version__ = "0.1.1"


class YubiStormError(Exception):
    """Raised for all kinds errors, that are above the https level.

    .. note::
        For http level errors, tornado.httpclient.HTTPError is raised instead.
    """
    pass


class YubiStormAPIError(YubiStormError):
    """Raised when YubiCloud API call returns an error.

    Instances of this class mean that they YubiCloud server already responded, and returned a status
    code that indicates a problem detected on the server side."""
    pass


class YubiStormSecurityBreachError(YubiStormError):
    """Raised when the client library detects possible security breach.

    Instances of this class mean that they YubiCloud server already responded, but there is a problem with the
    response: the client side detected a possible security breach."""
    pass


class YubiStorm(object):
    """Asynchronous YubiCloud authentication client that works with tornado."""
    """Clear this flag to disable validation of SSL certificates. (You should **NEVER** clear this flag.)"""
    validate_cert = True

    """User agent to be used for making requests to YubiCloud servers."""
    user_agent = "YubiStorm %s" % __version__
    """YubiCloud API servers."""
    api_servers = [
        "api.yubico.com",
        "api2.yubico.com",
        "api3.yubico.com",
        "api4.yubico.com",
        "api5.yubico.com",
    ]
    api_path = "/wsapi/2.0/"

    def __init__(self, client_id, client_secret, logger=None):
        """

        :param client_id: Your client id for your application.
        :param client_secret: Your base64 encoded API secret password for your custom application.
        :param logger: A logger object that will be used for logging.
        """
        self.http_client = tornado.httpclient.AsyncHTTPClient(defaults=dict(user_agent=self.user_agent))
        self.client_id = client_id
        self.client_secret = base64.b64decode(client_secret)
        self.logger = logger

    @classmethod
    def _create_new_nonce(cls):
        """Create a new unique unpredictable identifier.

        Used for the nonce parameter of YubiCloud API call.

        .. note::
            Although it is undocumented, the nonce parameter cannot contain any character that is escaped
            with % code in the GET request. For this reason, we are returning a hex digest here.
        """
        return uuid.uuid4().hex

    def create_signature(self, params):
        """Create HMAC_SHA1 signature for a query.

        :param params: A dict of GET parameter/name pairs.
        :return: The base64 encoded HMAC signature, as required by the YubiKey validation protocol.
            Please note that the returned value is **not a binary string**. It is a normal str instance.
        :rtype: str
        """
        data = []
        for key in sorted(params.keys()):
            data.append("%s=%s" % (key, params[key]))
        data = "&".join(data)
        if self.logger:
            self.logger.debug("create_signature: data: %s" % repr(data))
        hashed = hmac.new(self.client_secret, data.encode("ascii"), sha1)
        return base64.encodebytes(hashed.digest()).rstrip(b'\n').decode("ascii")

    def verify_signature(self, params):
        """Verify signature for a response.

        :param params: A dict of values as returned by the YubiCloud server.
            It should contain the hmac signature under the "h" key.
        :return: True if the signature was correct, False otherwise.
        """
        assert "h" in params
        bare = copy.copy(params)
        del bare["h"]
        good_signature = self.create_signature(bare)
        if self.logger:
            self.logger.debug("verify_signature: %s", good_signature == params["h"])
        return good_signature == params["h"]

    def _add_query_params(self, url, params, add_signature=True):
        """Add parameters to a GET url.

        :param url: The original GET url.
        :param params: A dict of parameters (name,value pairs)
        :param add_signature: When set, the HMAC-SHA1 signature will be added. (See YubiKey validation protocol.)
        :return: The modified url.

        Please note that this method does not support multiple values for the same parameter!
        """
        url_parts = list(urllib.parse.urlparse(url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        if add_signature:
            if "h" in query:
                del query["h"]
            query["h"] = self.create_signature(query)
        if self.logger:
            self.logger.debug("_add_query_params: %s", str(query))
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    async def get(self, rel_url, params, add_signature=True):
        """Get from YubiCloud.

        :param rel_url: URL relative path to api_path
        :param params: a dict of GET parameter values to be added to the GET url
        :param add_signature: Set flag to add hmac signature as parameter "h"
        :return: a response object

        This method sends a https GET request to one of the yubicloud servers and returns the response object.
        The server is selected randomly from ``api_servers``.

        This is an async method. You need to ``await`` for it. Do not call synchronously.
        """
        assert ("/" not in rel_url)
        server_host = random.choice(self.api_servers)
        api_url = "https://" + server_host + self.api_path
        url = self._add_query_params(api_url + rel_url, params, add_signature=add_signature)
        if self.logger:
            self.logger.debug("get: awaiting GET %s", url)
        request = tornado.httpclient.HTTPRequest(url=url, method="GET", validate_cert=self.validate_cert)
        response = await self.http_client.fetch(request)
        if self.logger:
            self.logger.debug("get: completed GET %s, code=%s reason='%s'", url, response.code, response.reason)
        if response.error:
            response.rethrow()
        else:
            return response

    async def get_and_parse(self, rel_url, params, add_signature=True):
        """Get from YubiCloud server and parse text response.

        :param rel_url: URL relative to api_url
        :param params: a dict of GET parameter values to be added to the GET url
        :param add_signature: Set flag to add hmac signature as parameter "h". Increases security (the server can
            verify the authenticity of the client).
        :return: a data structure, parsed from the response body text.

        This is an async method. You need to ``await`` for it. Do not call synchronously.

        **IMPORTANT:** before you use the response, you must also call verify_signature on it!
        """
        response = await self.get(rel_url, params, add_signature=add_signature)
        if self.logger:
            self.logger.debug("get_and_parse: response body:%s", response.body)
        txt = response.body.decode("UTF-8")
        result = {}
        for line in txt.split("\n"):
            line = line.strip()
            idx = line.find("=")
            assert idx
            name, value = line[:idx], line[idx + 1:]
            if name:
                result[name] = value
        # if not self.verify_signature(result):
        #    raise YubiStormSecurityBreachError("Signature verification failed on the server response.")
        return result

    @classmethod
    def is_valid_otp(cls, otp):
        """Check if the given otp value is an otp string that has a valid format.

        :param otp: A string containing the one time password, obtained from the YubiKey.

        Unfortunately, the modhex format used by YubiKey can be altered by a Drovak-based keyboard.
        YubiCo's recommendation is that we only check that the otp has 32-48 printable characters.
        """
        if isinstance(otp, str) and (32 <= len(otp) <= 48):
            return otp.isprintable()
        else:
            return False

    @classmethod
    def get_yubikey_id(cls, otp):
        """Get the unique identifier of a YubiKey from an otp.

        :param otp: A string containing the one time password, obtained from the YubiKey.

        Each YubiKey has a fixed unique identifier that is contained within the generated OTP. The YubiCloud service
        uses this identifier to identify the key, and store otp usage, detect replay attacks etc.

        This method extracts the unique identifier of the YubiKey from an otp generated with it. This identifier can
        be used assign the YubiKey to a user. Then it will be possible to find the user by giving just a single
        otp string (e.g. username input is not needed).
        """
        if not cls.is_valid_otp(otp):
            raise YubiStormAPIError("Invalid OTP: should be a printable string of 32-48 characters.")
        return otp[:-32]

    async def verify(self, otp, sl="secure"):
        """Veryify OTP value with YubiCloud server.

        :param otp: OTP value provided by a YubiKey hardware device.
        :param sl: securelevel value. When given, this should be an integer between 0 and 100,
                   indicating percentage of syncing required by client. You can also use strings "fast" or "secure"
                   to use server-configured values. If absent, let the server decide.
        :return: Returns a dict that contains a subset of the response from the server. Keys in the response:

                 * id - unique identifier of the yubikey
                 * timestamp - YubiKey internal timestamp when the key was pressed
                 * sessioncounter - YubiKey internal usage counter when key was pressed.
                        This will be a strictly increasing number that shows how many times the key was
                        pressed since it was first programmed.
                 * sessionuse - YubiKey internal session usage counter when key was pressed
                 * sl - percentage of external validation server that replied successfully (0 to 100)

        .. note::

            * When YubiCloud servers are not available, this method will raise a tornado.httpclient.HTTPError
            * When authentication is unsuccessful, this method will raise a YubiStormAPIError.

        """
        if not self.is_valid_otp(otp):
            raise YubiStormAPIError("Invalid OTP: should be a printable string of 32-48 characters.")
        nonce = self._create_new_nonce()
        params = {
            "id": self.client_id,
            "otp": otp,
            "nonce": nonce,
            "timestamp": "1",
        }
        if sl:
            if isinstance(sl, int):
                assert 0 <= sl <= 100
            else:
                assert sl in {"secure", "fast"}
            params["sl"] = sl
        result = await self.get_and_parse("verify", params)

        if result["status"].lower() != "ok":
            raise YubiStormAPIError(result["status"])

        if not self.verify_signature(result):
            raise YubiStormSecurityBreachError("Signature verification failed on the server response.")

        if result["nonce"] != nonce:
            raise YubiStormSecurityBreachError("Possible hijack of server response: nonce parameter was modified.")

        if result["otp"] != otp:
            raise YubiStormSecurityBreachError("Possible hijack of server response: otp parameter was modified.")

        return {
            "id": self.get_yubikey_id(otp),
            "timestamp": result["timestamp"],
            "sessioncounter": result["sessioncounter"],
            "sessionuse": result["sessionuse"],
            "sl": result["sl"],
        }
