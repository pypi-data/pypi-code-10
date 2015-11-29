import asyncio
import os

from aiohttp.web import Application

from aiohttp_apiset.routes import SwaggerRouter
from aiohttp_apiset.views import ApiSet


class View(ApiSet):
    swagger_ref = 'data/file.yaml#/paths/file'
    namespace = 'test'

    @asyncio.coroutine
    def get(self, request):
        return self.response({})


class Router(SwaggerRouter):
    def import_view(self, p: str):
        return View


def test_swagger_loader():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    app = Application(loop=loop)

    @asyncio.coroutine
    def run_test():
        router = Router(app=app)
        path = os.path.join(os.path.dirname(__file__), 'data/root.yaml')
        data = router.load_routes_from_swagger(path)  # noqa
        # import ipdb
        # ipdb.set_trace()

    loop.run_until_complete(run_test())
