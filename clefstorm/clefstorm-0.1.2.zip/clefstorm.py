"""Asynchronous client for Clef and Tornado."""
import sys
import json
import urllib.parse
from xml.sax.saxutils import quoteattr
from contextlib import contextmanager
import tornado
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    raise Exception("ClefStorm requires at least Python version 3.5.")
if tornado.version < "4.3":
    raise Exception("ClefStorm requires at least tornado version 4.3.")

__version__ = "0.1.2"


class ClefAPIError(Exception):
    """Raised when Clef API call returns an error."""
    pass


class ClefWaveStyle(object):
    """Represents the style of a Clef Wave."""

    def __init__(self, color="blue", style="button", custom=None, embed=None):
        """

        :param color: Color of the wave. Can be "blue" or "white".
        :param style: Style of the wave. Can be "flat" or "button".
        :param custom: With this option, won't generate a button, just attach the handlers to the element.
        :param embed: Display embedded wave instead of a button.
        """
        self.color = color
        self.style = style
        self.custom = custom
        self.embed = embed


"""Default wave style."""
DEFAULT_WAVE_STYLE = ClefWaveStyle()
"""All possible wave types."""
ALL_BUTTON_TYPES = ["login", "register", "connect"]


class BusTimeoutError(Exception):
    """Raised when the waiter has been waiting for too long."""
    pass


class AsyncBus(object):
    """Asynchronous notification bus.

    This is a helper class that is used for asynchronous notifications between http requests. You can await for
    notifications on a set of keys, and you can send notifications for waiters of a given key. This is similar to
    a Condition object, with the following differences:

     * AsyncBus.waitfor does have a timeout parameter (Condition does not)
     * AsyncBus can automatically route notifications to multiple waiters using message identifiers (keys).

    """

    def __init__(self):
        self._waiters = {}

    def notify(self, key, message):
        """Notify a single waiter.

        :param key: Key value that identifies the waiter. Should be immutable.
        :param message: The message to be delivered to the waiter.
        :return: True if the waiter was notified, False otherwise.
        """
        if key in self._waiters and self._waiters[key]:
            waiter = next(iter(self._waiters[key]))
            waiter.set_result((key, message))
            return True
        return False

    def notifyall(self, key, message):
        """Notify all waiters. Return the number of waiters notified.

        :param key: Key value that identifies the waiters. Should be immutable.
        :param message: The message to be delivered to the waiters.
        :return: The number of waiters notified
        :type: int
        """
        result = 0
        if key in self._waiters and self._waiters[key]:
            for waiter in iter(self._waiters[key]):
                waiter.set_result((key, message))
                result += 1
        return result

    @contextmanager
    def _listen(self, keys, waiter):
        # Add waiters to the dict of waiters
        for key in keys:
            if key in self._waiters:
                self._waiters[key].append(waiter)
            else:
                self._waiters[key] = [waiter]
        try:
            # Execute code
            yield
        finally:
            # Remove waiters from the dict of waiters
            for key in keys:
                if key in self._waiters:
                    self._waiters[key].remove(waiter)
                    if not self._waiters[key]:
                        del self._waiters[key]

    async def waitforkeys(self, keys, timeout=None):
        """Wait for notification.

        :param keys: An iterable that contains keys to be listened to. Keys should be immutable.
        :param timeout: If there is no notification coming in for the given timeout, then raise a BusTimeoutError.
        :return: A tuple of (key, message) that was sent by a notify() or notifyall() call.
        """
        waiter = tornado.concurrent.Future()
        with self._listen(keys, waiter):
            ioloop = tornado.ioloop.IOLoop.current()
            if timeout:
                handle = ioloop.add_timeout(timeout, lambda: waiter.set_exception(BusTimeoutError()))
            else:
                handle = None
            try:
                result = await waiter
            finally:
                if handle:
                    ioloop.remove_timeout(handle)
            return result

    async def waitforkey(self, key, timeout=None):
        """Wait for notification on a single key.

        :param key: An key to be listened to. Key should be immutable.
        :param timeout: If there is no notification coming in for the given timeout, then raise a BusTimeoutError.
        :return: A message that was sent by a notify() or notifyall() call.
        """
        _key, message = await self.waitforkeys([key], timeout)
        return message


class ClefStorm(object):
    """Asynchronous Clef authentication client that works with tornado."""
    """Clear this flag to disable validation of SSL certificates. (Not recommended.)"""
    validate_cert = True
    """After this timeout (seconds), token will invalidated from the cache. See `get_token`."""
    token_ttl = 3000.0

    """User agent to be used for making requests to www.clef.io"""
    user_agent = "ClefStorm %s" % __version__
    """Base URL of the Clef API"""
    api_url = "https://clef.io/api/v1/"

    _token_validuntil = 0
    _token = None

    def __init__(self, api_key, api_password, logger=None):
        """

        :param api_key: Your API key for your custom clef applicaiton.
        :param api_password: Your API secret password for your custom clef gapplicaiton.
        :param logger: A logger object that will be used for logging.
        """
        self.http_client = tornado.httpclient.AsyncHTTPClient(defaults=dict(user_agent=self.user_agent))
        self.api_key = api_key
        self.api_password = api_password
        self.logger = logger
        self.logout_eventbus = AsyncBus()

    @classmethod
    def _add_query_params(cls, url, params):
        """Add parameters to a GET url.

        :param url: The original GET url.
        :param params: A dict of parameters (name,value pairs)
        :return: The modified url.

        Please note that this method does not support multiple values for the same parameter!
        """
        url_parts = list(urllib.parse.urlparse(url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    def generate_button(self, redirect_url, state, typ="login", style=None):
        """Generate a Clef Wave that can be used for login, registration or connection.

        :param redirect_url: The URL where the user's browser should be redirected after successful authentication.
            This should not contain any GET parameters, nor the ? character at the end.
        :param state: XSFR token - unpredictable random string that will be used against cross site forgery attacks.
        :param typ: Type of the wave, can be "login", "register" or "connect".
        :param style: A ClefWaveStyle instance.
        :return: Javascript code for the button.
        """
        if not style:
            style = DEFAULT_WAVE_STYLE
        assert (typ in ALL_BUTTON_TYPES)
        redirect_url = self._add_query_params(redirect_url, {"state": state})
        settings = {
            "data-app-id": self.api_key,
            "data-color": style.color,
            "data-style": style.style,
            "data-type": typ,
            "data-redirect-url": redirect_url,
            "class": "clef-button",
            "src": "https://clef.io/v3/clef.js",
            "type": "text/javascript",
        }
        return '<script ' + ' '.join(
            ['%s=%s' % (attrname, quoteattr(settings[attrname])) for attrname in settings]
        ) + '></script>'

    async def get(self, rel_url, params):
        """Get from Clef.

        :param rel_url: URL relative to api_url
        :param params: a dict of GET parameter values to be added to the GET url
        :return: a response object
        """
        assert ("/" not in rel_url)
        url = self._add_query_params(self.api_url + rel_url, params)
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

    async def get_and_parse(self, rel_url, params):
        """Get from Clef and parse json response.

        :param rel_url: URL relative to api_url
        :param params: a dict of GET parameter values to be added to the GET url
        :return: a data structure, parsed by json.loads from the response body.
        """
        response = await self.get(rel_url, params)
        if self.logger:
            self.logger.debug("get_and_parse: response body:%s", response.body)
        data = json.loads(response.body.decode("UTF-8"))
        if data["success"]:
            return data
        else:
            raise ClefAPIError(data["error"])

    async def post(self, rel_url, params):
        """Post params to Clef

        :param rel_url: URL relative to api_url
        :param params: A dict of POST parameters
        :return: a response object
        """
        assert ("/" not in rel_url)
        url = self.api_url + rel_url
        body = urllib.parse.urlencode(params)
        if self.logger:
            self.logger.debug("post: awaiting POST %s body=%s", url, body[:100])
        request = tornado.httpclient.HTTPRequest(url=url, method="POST", body=body, validate_cert=self.validate_cert)
        response = await self.http_client.fetch(request)
        if self.logger:
            self.logger.debug("post: completed POST %s, code=%s reason='%s'", url, response.code, response.reason)
        if response.error:
            response.rethrow()
        else:
            return response

    async def post_and_parse(self, rel_url, params):
        """Post to Clef and parse json response.

        :param rel_url: URL relative to api_url
        :param params: a dict of GET parameter values to be added to the GET url
        :return: a data structure, parsed by json.loads from the response body.
        """
        response = await self.post(rel_url, params)
        if self.logger:
            self.logger.debug("post_and_parse: response body:%s", response.body)
        data = json.loads(response.body.decode("UTF-8"))
        if data["success"]:
            return data
        else:
            raise ClefAPIError(data["error"])

    async def get_token(self, code):
        """Exchange authorization code into an access token.

        :param code: Authorization code from the login GET callback.
        :return: access token
        :rtype: str
        """
        params = dict(code=code, app_id=self.api_key, app_secret=self.api_password)
        data = await self.post_and_parse("authorize", params)
        return data["access_token"]

    async def get_info(self, access_token):
        """Get information about the logged in user.

        :param access_token: Access token as returned by get_token()
        :return: User information
        :rtype: dict
        """
        params = dict(access_token=access_token)
        data = await self.get_and_parse("info", params)
        return data["info"]

    async def get_logged_out_clef_id(self, logout_token):
        """Exchange a logout token with a clef id that needs to be logged out.

        :param logout_token: The logout token, provided by the clef logout webhook callback.
        :return: A clef id that needs to be logged out.
        :rtype: int
        """
        params = dict(logout_token=logout_token, app_id=self.api_key, app_secret=self.api_password)
        data = await self.post_and_parse("logout", params)
        return data["clef_id"]

    def notify_logout(self, clef_id):
        """Notify all clients (browsers) that the user has been logged out remotely.

        :param clef_id: The clef id of the user that was logged out.
        :return: Number of waiters notified.
        """
        return self.logout_eventbus.notifyall(clef_id, clef_id)  # (key, message)

    async def wait_for_logout(self, clef_id, timeout):
        """Wait until a user is logged out.

        :param clef_id: The clef id of the user who is waiting for a logout callback from Clef.
        :param timeout: A datetime.timedelta instance.After the given timeout, a BusTimeoutError
            will be raised.
        :return: The clef id of the user that was logged out
        :rtype: int
    """
        return await self.logout_eventbus.waitforkey(clef_id, timeout)
