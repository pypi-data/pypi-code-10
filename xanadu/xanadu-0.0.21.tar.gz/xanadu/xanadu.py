#!/usr/bin/env python
# encoding=utf-8

import os
import sys
import cgi
import types
import traceback
import mimetypes
import functools

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from .errors import *
from .util import *
from .request import Request
from .response import Response

__author__ = 'xlzd'


def get(path):
    """
    @get
    """
    def decorator(function):
        function.__web_route__ = path
        function.__methods__ = ['GET']
        return function
    return decorator


def post(path):
    """
    @post
    """
    def decorator(function):
        function.__web_route__ = path
        function.__methods__ = ['POST']
        return function
    return decorator


_RE_ROUTE = re.compile(ur'(<:[A-Za-z_]\w*>)')


def _build_regex(path):
    """
    path -> regex
    """
    regex_list = []
    var_list = []
    is_var = False
    for var in _RE_ROUTE.split(path):
        if is_var:
            var_name = var[2:-1]
            var_list.append(var_name)
            regex_list.append(r'(?P<%s>[^\/]+)' % var_name)
        else:
            s = reduce(lambda s, ch: s + ('\\' + ch, ch)[ch.isdigit() or ch.isalpha()], var, '')
            regex_list.append(s)
        is_var = not is_var
    regex_list.append('$')
    return ''.join(regex_list)


class Route(object):
    """
    route
    """
    def __init__(self, function):
        self._path = function.__web_route__
        self._methods = function.__methods__
        self._is_static = _RE_ROUTE.search(self._path) is None
        if not self._is_static:
            regex = _build_regex(self._path)
            print 'regex at route :', regex
            self.regex = regex
            self._route = re.compile(regex)
        self._function = function

    @property
    def path(self):
        return self._path

    @property
    def is_static(self):
        return self._is_static

    @property
    def methods(self):
        return self._methods

    def match(self, url):
        match = self._route.search(url)
        if match:
            return match.groups()
        return None

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

    def __str__(self):
        route_type = ('dynamic', 'static')[self._is_static]
        return 'Route({type}, [{method}], {path})'.format(type=route_type, method=', '.join(self._methods), path=self._path)

    __repr__ = __str__


BLOCK_SIZE = 8192


def _static_file_generator(file_path):
    with open(file_path, 'rb') as fp:
        block = fp.read(BLOCK_SIZE)
        while block:
            yield block
            block = fp.read(BLOCK_SIZE)


class StaticFileRoute(object):

    def __init__(self):
        self._methods = ['GET']
        self._is_static = False
        self._route = re.compile('^/static/(.+)$')

    @classmethod
    def match(cls, url):
        if url.startswith('/static/'):
            return url[1:],
        return None

    def __call__(self, *args, **kwargs):
        file_path = os.path.join(context.application.document_root, args[0])
        if not os.path.isfile(file_path):
            raise notfound()
        suffix = os.path.splitext(file_path)[1].lower()
        context.response.content_type = mimetypes.types_map.get(suffix, 'application/octet-stream')
        return _static_file_generator(file_path)


class MultipartFile(object):
    """
    multipart file.
    f = ctx.request['file']
    f.filename # 'test.png'
    f.file # file-like object
    """
    def __init__(self, storage):
        self._filename = to_unicode(storage.filename)
        self.file = storage.file


class Template(object):

    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.model = dict(**kwargs)


class TemplateEngine(object):

    def __call__(self, path, model):
        return '<!-- override this method to reder template -->'


class Jinja2TemplateEngine(TemplateEngine):

    def __init__(self, template_dir, **kwargs):
        from jinja2 import Environment, FileSystemLoader
        if not 'autoescape' in kwargs:
            kwargs['authescape'] = True
        self._env = Environment(loader=FileSystemLoader(template_dir), **kwargs)

    def add_filter(self, name, filter):
        self._env.filters[name] = filter

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')


def _default_error_handler(e, start_response, is_debug):
    if isinstance(e, HTTPError):
        # TODO logging.info e.status
        headers = e.headers[:]
        headers.append(('Content-Type', 'text/html'))
        start_response(e.status, headers)
        return '<html><body><h1>%s</h1></body></html>' % e.status
    # TODO logging
    start_response('500 Internal Server Error', [('Content-Type', 'text/html'), HEADER_X_POWERED_BY])
    if is_debug:
        return _debug()
    return '<html><body><h1>500 Internal Server Error</h1><h3>%s</h3></body></html>' % str(e)


def view(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                # TODO logging
                return Template(path, **result)
            raise ValueError('Expect return a dict when using @view() decorator.')
        return wrapper
    return decorator


def _build_pattern_fn(pattern):
    m = RE_INTERCEPTROR_STARTS_WITH.match(pattern)
    if m:
        return lambda p: p.startswith(m.group(1))
    m = RE_INTERCEPTROR_ENDS_WITH.match(pattern)
    if m:
        return lambda p: p.endswith(m.group(1))
    raise ValueError('Invalid pattern definition in interceptor.')


def interceptor(pattern='/'):
    """
    @interceptor('/admin/')
    def check_admin(req, resp):
        pass
    """
    def decorator(func):
        func.__interceptor__ = _build_pattern_fn(pattern)
        return func
    return decorator


def _build_interceptor_fn(func, next):
    def wrapper():
        if func.__interceptor__(context.request.path_info):
            return func(next)
        else:
            return next()
    return wrapper


def _build_interceptor_chain(last_fn, *interceptors):
    """
    Build interceptor chain.
    >>> def target():
    ...     print 'target'
    ...     return 123
    >>> @interceptor('/')
    ... def f1(next):
    ...     print 'before f1()'
    ...     return next()
    >>> @interceptor('/test/')
    ... def f2(next):
    ...     print 'before f2()'
    ...     try:
    ...         return next()
    ...     finally:
    ...         print 'after f2()'
    >>> @interceptor('/')
    ... def f3(next):
    ...     print 'before f3()'
    ...     try:
    ...         return next()
    ...     finally:
    ...         print 'after f3()'
    >>> chain = _build_interceptor_chain(target, f1, f2, f3)
    >>> ctx.request = Dict(path_info='/test/abc')
    >>> chain()
    before f1()
    before f2()
    before f3()
    target
    after f3()
    after f2()
    123
    >>> ctx.request = Dict(path_info='/api/')
    >>> chain()
    before f1()
    before f3()
    target
    after f3()
    123
    """
    lst = list(interceptors)
    lst.reverse()
    fn = last_fn
    for f in lst:
        fn = _build_interceptor_fn(f, fn)
    return fn


def _load_module(module_name):
    last_dot = module_name.rfind('.')
    if last_dot == (-1):
        return __import__(module_name, globals(), locals())

    from_module = module_name[:last_dot]
    import_module = module_name[last_dot + 1:]
    m = __import__(from_module, globals(), locals(), [import_module])
    return getattr(m, import_module)


class WSGIApplication(object):

    def __init__(self, document_root=None, **kwargs):
        self._running = False
        self._document_root = document_root

        self._interceptors = []
        self._template_engine = None

        self._get_static = {}
        self._post_static = {}

        self._get_dynamic = []
        self._post_dynamic = []

    def _check_not_running(self):
        if self._running:
            raise RuntimeError('Cannot modify WSGIApplication when running.')

    @property
    def template_engine(self):
        return self._template_engine

    @template_engine.setter
    def template_engine(self, engine):
        self._check_not_running()
        self._template_engine = engine

    def add_module(self, module):
        self._check_not_running()
        m = module if types.ModuleType == type(module) else _load_module(module)
        # TODO logging add module
        for name in dir(m):
            fn = getattr(m, name)
            if callable(fn) and hasattr(fn, '__web_route__') and hasattr(fn, '__web_methods__'):
                self.add_url(fn)

    def add_url(self, function):
        self._check_not_running()
        route = Route(function)
        print 'route.path :', route.path
        print 'route :', route
        if route.is_static:
            for method in route.methods:
                if method == 'GET':
                    self._get_static[route.path] = route
                elif method == 'POST':
                    self._post_static[route.path] = route
        else:
            for method in route.methods:
                if method == 'GET':
                    # self._get_dynamic[route.path] = route
                    self._get_dynamic.append(route)
                elif method == 'POST':
                    # self._post_dynamic[route.path] = route
                    self._post_dynamic.append(route)

    def add_interceptor(self, function):
        self._check_not_running()
        self._interceptors.append(function)

    def run(self, port=44443, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application(debug=True))
        print 'Server run at %s:%s' % (host, port)
        server.serve_forever()

    def get_wsgi_application(self, debug=False):
        self._check_not_running()
        if debug:
            self._get_dynamic.append(StaticFileRoute())
        self._running = True
        _application = {'document_root': self._document_root}

        def fn_route():
            request_method = context.request.request_method
            path_info = context.request.path_info

            if request_method == 'GET':
                fn = self._get_static.get(path_info, None)
                if fn:
                    return fn()
                for fn in self._get_dynamic:
                    print 'matching fn :', fn.regex, path_info
                    args = fn.match(path_info)
                    if args:
                        return fn(*args)
                raise notfound()
            if request_method == 'POST':
                fn = self._post_static.get(path_info, None)
                if fn:
                    return fn()
                for fn in self._post_dynamic:
                    args = fn.match(path_info)
                    if args:
                        return fn(*args)
                raise notfound()
            raise badrequest()

        fn_exec = _build_interceptor_chain(fn_route, *self._interceptors)

        def wsgi(env, start_response):
            context.application = _application
            context.request = Request(env)
            response = context.response = Response()
            try:
                r = fn_exec()
                if isinstance(r, Template):
                    r = self._template_engine(r.template_name, r.model)
                if isinstance(r, unicode):
                    r = r.encode('utf-8')
                if r is None:
                    r = []
                start_response(response.status, response.headers)
                return r
            except RedirectError, e:
                response.set_header('Location', e.location)
                start_response(e.status, response.headers)
                return []
            except HTTPError, e:
                start_response(e.status, response.headers)
                return ['<html><body><h1>%s</h1></body></html>' % e.status]
            except Exception, e:
                # TODO loggin exception
                if not debug:
                    start_response('500 Internal Server Error', [])
                    return ['<html><body><h1>500 Internal Server Error</h1></body></html>']
                exc_type, exc_value, exc_traceback = sys.exc_info()
                fp = StringIO()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=fp)
                stacks = fp.getvalue()
                fp.close()
                start_response('500 Internal Server Error', [])
                return [
                    r'''<html><body><h1>500 Internal Server Error</h1><div style="font-family:Monaco, Menlo, Consolas, 'Courier New', monospace;"><pre>''',
                    stacks.replace('<', '&lt;').replace('>', '&gt;'),
                    '</pre></div></body></html>'
                ]
            finally:
                del context.application
                del context.request
                del context.response
        return wsgi


if __name__ == '__main__':
    print _build_regex('/user/<:id>')
    # print _RE_ROUTE.search('/user/id') is None

