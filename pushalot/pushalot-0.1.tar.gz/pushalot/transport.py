import json
from abc import (
    ABCMeta,
    abstractmethod,
)
from six import (
    with_metaclass,
    reraise,
)
try:
    from urllib.request import urlopen
    from urllib.parse import ( # pragma: no cover
        urlparse,
        urlencode,
    )
    from urllib.error import URLError # pragma: no cover
except ImportError: # pragma: no cover
    from urlparse import urlparse # pragma: no cover
    from urllib2 import ( # pragma: no cover
        urlopen,
        URLError,
    )
    from urllib import urlencode # pragma: no cover

import pushalot.exc

API_URL = 'https://pushalot.com/api/sendmessage'

class PushalotTransportInterface(with_metaclass(ABCMeta)):

    @abstractmethod # pragma: no cover
    def send(self, **kwargs):
        """Send request to API

        Only this method required. Method receives
        dictionary with api requests params, and
        send request.
        Should return True if request successfully sent,
        or throw exception on failure.

        :raises PushalotBadRequestException: Bad parameters sent to API
        :raises PushalotNotAcceptableException: API message throttle limit hit
        :raises: PushalotGoneException: Invalid or blocked authorization token
        :raises PushalotInternalErrorException: API server error
        :raises PushalotUnavailableException: API server unavailable
        :param kwargs: Dictionary with API request parameters
        :type kwargs: dict
        :return: True on success
        :rtype: bool
        """

class HTTPTransport(PushalotTransportInterface):

    def _send_http_request(self, **kwargs):
        try:
            params = urlencode(kwargs)
            response = urlopen(url=API_URL, data=params.encode('utf-8'))
        except URLError as e:
            response = e

        body = "\n".join([x.decode('utf-8') for x in response.readlines()])
        code = response.code
        response.close()
        return code, body

    def send(self, **kwargs):
        code = None
        try:
            code, body = self._send_http_request(**kwargs)
            decoded = json.loads(body)
        except Exception as e:
            import sys
            reraise(
                pushalot.exc.PushalotException,
                pushalot.exc.PushalotException(
                    'Uncaught API exception: {}'.format(str(e))
                ),
                sys.exc_info()[2]
            )

        if code == 200:
            if decoded['Success'] == False:
                raise pushalot.exc.PushalotException(
                    "Uncaught error occupied: {}".format(decoded['Description'])
                )
            return True
        elif code == 400:
            raise pushalot.exc.PushalotBadRequestException(
                decoded['Description']
            )
        elif code == 406:
            raise pushalot.exc.PushalotNotAcceptableException(
                decoded['Description']
            )
        elif code == 410:
            raise pushalot.exc.PushalotGoneException(
                decoded['Description']
            )
        elif code == 500:
            raise pushalot.exc.PushalotInternalErrorException()
        elif code == 503:
            raise pushalot.exc.PushalotUnavailableException()
        else:
            raise pushalot.exc.PushalotException(
                'Unknown HTTP code returned'
            )
