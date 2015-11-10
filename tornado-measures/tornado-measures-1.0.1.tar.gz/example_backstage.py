from tornado.ioloop import IOLoop
from tornado import gen
from tornado_measures import setup_measures
from tornado.httpclient import AsyncHTTPClient

setup_measures(
    client='backstage_apis_test',  # TSURU_APPNAME
    address=('logstash.measures.backstage.qa01.globoi.com', 1984)
)

http_client = AsyncHTTPClient()


@gen.coroutine
def blah():
    response = yield http_client.fetch(
        "https://accounts.backstage.qa01.globoi.com/", raise_error=True)

blah()
IOLoop.current().start()
