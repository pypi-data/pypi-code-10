import requests

import posixpath
from urlparse import urlunparse
from urllib import urlencode

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl


class TLSv1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def get_pin_url(token, pin, fields=[]):
    """
    Construct the URL that will obtain the data
    for the specified pin
    """
    path = posixpath.sep.join(["v1/pins", pin])
    query = {"access_token": token}
    if fields:
        query["fields"] = ",".join(fields)

    return urlunparse((
        "https", "api.pinterest.com", path,
        "", urlencode(query), ""
    ))


class APIClient(object):
    """
    This client obtains the full pin details by
    using the Pinterest API
    """

    # By default, just grab all available fields
    DEFAULT_FIELDS = ["id", "link", "url", "creator",
                      "board", "created_at", "note",
                      "color", "counts", "media",
                      "attribution", "image",
                      "metadata"]

    def __init__(self, token):
        self.token = token
        self.req = requests.Session()
        self.req.mount("https://", TLSv1Adapter())

    def get_pin(self, pin_id, fields=DEFAULT_FIELDS):
        url = get_pin_url(self.token, pin_id, fields)
        return self.req.get(url).json()
