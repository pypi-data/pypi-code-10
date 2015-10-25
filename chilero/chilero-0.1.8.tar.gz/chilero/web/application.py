import asyncio
import os

from aiohttp import hdrs, web
from aiohttp.web_urldispatcher import UrlDispatcher
from chilero.web.resource import Resource


class Application(web.Application):

    def __init__(self, routes=None, **kwargs):
        super(Application, self).__init__(**kwargs)

        for route in routes or []:
            self.register_routes(route)

    def dispatcher(self, cls, method):
        @asyncio.coroutine
        def f(request, *args, **kwargs):
            vkwargs = dict()
            for k in request.match_info.keys():
                vkwargs[k] = request.match_info.get(k)
            return getattr(
                cls(request, self, *args, **kwargs), method
            )(**vkwargs)

        return f

    def register_routes(self, route):
        pattern = route[0]
        view = route[1]

        already_registered = []
        name_already_registered = []
        if issubclass(view, Resource):
            # Add resource actions as urls

            url_name = route[2] \
                if len(route) == 3 \
                else view.resource_name \
                if hasattr(view, 'resource_name') \
                else view.__name__.lower()

            object_pattern = r'%s' % os.path.join(pattern, view.id_pattern)

            patterns = {
                # Collection's actions to HTTP methods mapping
                pattern: dict(
                    index=[hdrs.METH_GET],
                    new=[hdrs.METH_POST, hdrs.METH_PUT],
                ),
                # Element's actions to HTTP methods mapping
                object_pattern: dict(
                    show=[hdrs.METH_GET],
                    update=[hdrs.METH_PUT, hdrs.METH_PATCH],
                    destroy=[hdrs.METH_DELETE]
                )

            }

            for pt, actions in patterns.items():
                for action, methods in actions.items():
                    if callable(getattr(view, action, None)):
                        for method in methods:
                            already_registered.append((pt, method.lower()))
                            name = '{}_{}'.format(
                                url_name, 'index' if pt == pattern else 'item'
                            )
                            if (name, pt) in name_already_registered:
                                name = None
                            else:
                                name_already_registered.append((name, pt))
                            self.router.add_route(
                                method, pt, self.dispatcher(view, action),
                                name=name
                            )

        else:
            # Its a basic view
            url_name = route[2] \
                if len(route) == 3 \
                else view.__name__.lower()

            # HTTP methods as lowercase view methods
            for method in UrlDispatcher.METHODS:

                if callable(getattr(view, method.lower(), None)) \
                        and not (pattern, method) in already_registered:
                    # Do not bind the same method twice

                    name = url_name

                    if (name, pattern) in name_already_registered:
                        name = None  # pragma: no cover
                    else:
                        name_already_registered.append((name, pattern))

                    self.router.add_route(
                        method,
                        pattern,
                        self.dispatcher(view, method.lower()),
                        name=name
                        )

    def reverse(self, name, query=None, **kwargs):
        assert name in self.router, "Url '{}' doesn't exists!".format(name)
        if kwargs:
            return self.router[name].url(parts=kwargs, query=query)
        else:
            return self.router[name].url(query=query)
