import json

from json_url_rewriter import config
from json_url_rewriter.rewrite import URLRewriter


class HeaderToPathPrefixRewriter(object):
    """
    A rewriter to take the value of a header and prefix any path.
    """

    def __init__(self, keys, base, header_name):
        self.keys = keys
        self.base = base
        self.header_name = header_name

    @property
    def regex(self):
        return '(%s)(.*)' % self.base

    def header(self):
        return 'HTTP_' + self.header_name.upper().replace('-', '_')

    def __call__(self, doc, environ):
        key = self.header()
        if not key in environ:
            return doc

        prefix = environ[key]

        def replacement(match):
            base, path = match.groups()
            return '%s/%s%s' % (base, prefix, path)

        rewriter = URLRewriter(self.keys, self.regex, replacement)
        return rewriter(doc)


class RewriteMiddleware(object):

    def __init__(self, app, rewriter):
        self.app = app
        self.rewriter = rewriter

    @staticmethod
    def content_type(headers):
        return dict([(k.lower(), v) for k, v in headers]).get('content-type')

    def is_json(self, headers):
        return 'json' in self.content_type(headers)

    @staticmethod
    def ok(status):
        return status.startswith('20')

    def rewrite(self, resp, environ):
        doc = self.rewriter(self.json(resp), environ)
        return json.dumps(doc)

    def json(self, resp):
        return json.loads(''.join(resp))

    def __call__(self, environ, start_response):
        # Set a local variable for the request
        self.do_rewrite = False

        # Our request local start response wrapper to grab the
        # response headers
        def sr(status, response_headers, exc_info=None):
            if self.ok(status) and self.is_json(response_headers):
                self.do_rewrite = True
            # Call the original start_response
            return start_response(status, response_headers, exc_info)

        # call our app
        resp = self.app(environ, sr)

        # Our local variable should have been set to True if we should
        # rewrite
        if self.do_rewrite:
            return [self.rewrite(resp, environ)]

        return resp
