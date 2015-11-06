from zope.interface import implements

import treq
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from vumi.tests.helpers import IHelper


class SiteHelper(object):
    """ Helper for testing HTTP Sites.

    :type site:
        twisted.web.server.Site
    :param site:
        Site to server.
    :type treq_kw:
        Function
    :param treq_kw:
        Callback function for generating treq request arguments. Any keyword
        arguments passed to the request helper methods are passed to this
        callback and the returned dictionary is passed to the underlying treq
        request function. The default function simple returns the keyword
        arguments as given.
    """

    implements(IHelper)

    def __init__(self, site, treq_kw=None):
        self.site = site
        self.server = None
        self.url = None
        self.treq_kw = treq_kw
        if self.treq_kw is None:
            self.treq_kw = lambda **kw: kw

    @inlineCallbacks
    def setup(self):
        self.server = yield reactor.listenTCP(0, self.site)
        addr = self.server.getHost()
        self.url = "http://%s:%s" % (addr.host, addr.port)

    @inlineCallbacks
    def cleanup(self):
        if self.server is not None:
            yield self.server.loseConnection()

    def _call(self, handler, path, **kw):
        url = "%s%s" % (self.url, path)
        kw = self.treq_kw(**kw)
        return handler(url, persistent=False, **kw)

    def get(self, path, **kw):
        return self._call(treq.get, path, **kw)

    def post(self, path, **kw):
        return self._call(treq.post, path, **kw)

    def put(self, path, **kw):
        return self._call(treq.put, path, **kw)

    def delete(self, path, **kw):
        return self._call(treq.delete, path, **kw)
