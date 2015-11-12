import urllib2
import json

from ..functions.operators import repeat_call

def repeat_read_url_request(url, headers=None, data=None, retries=2, logger=None):
    if logger:
        logger.debug("Retrieving url content: {}".format(url))
    req = urllib2.Request(url, data, headers=headers or {})
    return repeat_call(lambda: urllib2.urlopen(req).read(), retries)

def repeat_read_json_url_request(url, headers=None, data=None, retries=2, logger=None):
    if logger:
        logger.debug("Retrieving url json content: {}".format(url))
    req = urllib2.Request(url, data=data, headers=headers or {})
    return repeat_call(lambda: json.loads(urllib2.urlopen(req).read()), retries)
