import time

from prometheus_client import start_http_server, Histogram, Counter
from pyramid.tweens import EXCVIEW

_pyramid_request_latency = Histogram('pyramid_request_latency', 'Latency of requests', ['method', 'route', 'status'])
_pyramid_request_total = Counter('pyramid_requests_total', 'HTTP Requests', ['method', 'route', 'status'])

def tween_factory(handler, registry):
    def tween(request):
        start = time.time()
        status = '500'
        try:
            response = handler(request)
            status = str(response.status_int)
            return response
        finally:
            if request.matched_route is None:
                route_name = ''
            else:
                route_name = request.matched_route.name
            label_values = (request.method, route_name, status)
            _pyramid_request_latency.labels(*label_values).observe(time.time() - start)
            _pyramid_request_total.labels(*label_values).inc()
    return tween


def includeme(config):
    settings = config.registry.settings
    port = settings.get('prometheus.port', None)
    if port:
        # if you don't specify port, you have to expose the metrics yourself somehow
        start_http_server(int(port))
    config.add_tween('pyramid_prometheus.tween_factory', over=EXCVIEW)
