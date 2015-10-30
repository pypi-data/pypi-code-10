from pyramid.request import Request


class Requestable(object):

    def feed_request(self, request):
        self._convert_request(request)

    def _convert_request(self, request):
        cls = self._get_request_cls()
        if type(request) is cls:
            self.request = request
        else:
            self.request = cls(request)

    def _get_request_cls(self):
        return ImpafRequest

    @property
    def registry(self):
        return self.request.registry

    @property
    def POST(self):
        return self.request.POST

    @property
    def GET(self):
        return self.request.GET

    @property
    def matchdict(self):
        return self.request.matchdict

    @property
    def route_path(self):
        return self.request.route_path

    @property
    def settings(self):
        return self.registry['settings']

    @property
    def paths(self):
        return self.registry['paths']


class ImpafRequest(Request):

    def __init__(self, request):
        self.__dict__ = request.__dict__
        self._cache = {}

    @property
    def settings(self):
        return self.registry['settings']

    @property
    def paths(self):
        return self.registry['paths']
