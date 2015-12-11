import json
import urllib2
import urlparse

import SimpleTCPClientException

from Method import _Method

__author__ = 'umairghani'


class SimpleTCPClient(object):
    """
    Client class for a logical connection
    to the TCP Server
    """
    def __init__(self, host, port=80, ssl=False):
        """
        Constructor
        :param host:
        :param port:
        """
        self.url = "%s://%s:%d" % ('https' if ssl else 'http', host, port)
        self.methods = self._listMethods()

    def _uri(self, request):
        """
        opens the URL
        :param request:
        :return: response
        """
        try:
            _output = urllib2.urlopen(request)
            return _output.read()
        except urllib2.HTTPError, e:
            raise SimpleTCPClientException.HTTPError(e)
        except urllib2.URLError, e:
            raise SimpleTCPClientException.URLError(e)

    def _get(self, url):
        """
        HTTP GET private class
        :return: response
        """
        _request = urllib2.Request(url)
        return self._uri(_request)

    def get(self, url):
        """
        HTTP GET Public function
        :param url:
        :return: response
        """
        _url = urlparse.urljoin(self.url, url)
        return self._get(_url)

    def post(self, data):
        """
        HTTP POST
        :param data:
        :return: response
        """
        _data = json.dumps(data)
        _request = urllib2.Request(self.url)
        _request.add_header("Content-type", "application/json")
        _request.add_data(_data)
        return self._uri(_request)

    def geturl(self):
        """
        :return: the base url
        """
        return self.url

    def _listMethods(self):
        """
        List all the methods on the server
        :return: List of methods
        """
        #_functions = {}
        _url = urlparse.urljoin(self.url, "list_methods")
        _response = self._get(_url)
        return json.loads(_response)["list_methods"]
        #for _method in _methods:
        #    _functions[_method] = _method
        #return _functions

    def _request(self, method, data):
        """
        Call a method on the remote server
        :param method:
        :param data:
        :return: response
        """
        __params = {method: data}
        __response = self.post(__params)
        return __response

    def __getattr__(self, item):
        """
        Magic method dispatcher
        :param item:
        :return: response
        """
        return _Method(self._request, item)

    def __dir__(self):
        _methods = ["post", "get", "geturl"]
        _methods.extend(self.methods)
        return _methods
