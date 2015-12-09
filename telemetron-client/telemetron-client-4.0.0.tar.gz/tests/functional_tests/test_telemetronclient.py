from nose.tools import assert_raises


def test_expect_correct_metric_format_over_real_api():
    import SocketServer
    import threading
    import SimpleHTTPServer
    import time

    from telemetronclient.telemetronclient import TelemetronClient
    from .helpers import ThreadedTCPServer

    prefix = "prefix"
    namespace = "ns"
    metric = "metric"
    value = 10
    token = "token"
    app = "app"
    tags = {'tag1': 'val1', 'tag2': 'val2'}
    timestamp = int(time.time())

    class MockHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        """
        Class used by HTTP mock server to handle requests.
        """

        def do_PUT(self):
            """ Returns a dummy HTTP response to PUT requests
            (see SimpleHTTPRequestHandler) """
            import re

            data = self.rfile.read(int(self.headers.get('Content-Length')))
            pat = r"%(prefix)s.%(namespace)s.%(metric)s.* %(value)d.* "+\
                "%(timestamp)d"
            pat = pat % {
                'prefix': prefix,
                'namespace': namespace,
                'metric': metric,
                'value': value,
                'timestamp': timestamp
                }

            # Check string for all tags
            tags_exist = ["%s=%s" % (key, val) for key, val in tags.items()]

            if re.match(pat, data) and all(tags_exist):
                self.send_response(201)
            else:
                self.send_response(500)

            self.send_header("Content-Length", 0)
            self.end_headers()

    server = ThreadedTCPServer(("localhost", 4443), MockHTTPHandler)
    server.thread = threading.Thread(target=server.serve_forever)
    server.thread.daemon = True
    server.thread.start()

    client = TelemetronClient(settings={
        'dryrun': False,
        'prefix': prefix,
        'transport': TelemetronClient.TRANSPORT_API,
        'token': token,
        'app': app,
        'host': 'localhost',
        'port': 4443,
        'flush_size': 999
        })

    client.put(metric, value, tags, namespace=namespace, timestamp=timestamp)
    assert client.flush()

    server.shutdown()
    server.server_close()
    server.thread.join()

    return server


def test_expect_buffer_persistence_after_broken_socket():
    from Queue import Queue
    from Queue import Empty
    import re

    from .helpers import setup_tcp_server

    def socket_close_and_buffer_persistence(transport, method, count=2):
        from random import randint
        from telemetronclient.telemetronclient import TelemetronClient
        from telemetronclient.utils.map import Map

        client = TelemetronClient(settings=Map({
            'dryrun': False,
            'prefix': '%s_prefix' % (transport,),
            'transport': transport,
            'app': '%s_app' % (transport,),
            'host': 'localhost',
            'port': 2013
            }))

        func = getattr(client, method)
        for i in range(count):
            func("%s%d" % (method, i,), randint(1, 100))

        client._socket.close()  # Simulate disconnected client
        client._socket = None  # Reestablish connection
        client.init_transport()

        assert client.buffer_count == count
        client.flush()
        assert client.buffer_count == 0

    for method in ["timer", "gauge", "counter"]:
        for transport in ["tcp"]:
            incoming = Queue()
            server = setup_tcp_server(incoming)

            yield socket_close_and_buffer_persistence, transport, method
            lines = []
            while 1:
                try:
                    lines.append(incoming.get(timeout=0.1))
                except Empty:
                    break

            server.shutdown()
            server.server_close()
            server.thread.join()

            assert len(lines) == 2

            pat = r"%(transport)s_prefix.application.%(method)s" + \
                ".%(method)s.* .* .*"
            pat = pat % {'method': method, 'transport': transport}

            assert re.match(pat, lines[0]) is not None


def test_expect_real_client_to_auto_flush():
    from Queue import Queue
    from Queue import Empty

    from .helpers import setup_tcp_server

    def auto_flush(transport, method, flush_size=5, count=11):
        from random import randint
        from telemetronclient.telemetronclient import TelemetronClient
        from telemetronclient.utils.map import Map

        client = TelemetronClient(settings=Map({
            'dryrun': False,
            'prefix': '%s_prefix' % (transport,),
            'transport': transport,
            'app': '%s_app' % (transport,),
            'host': 'localhost',
            'port': 2013,
            'flush_size': flush_size
            }))

        func = getattr(client, method)

        for i in range(count):
            func("%s%d" % (method, i,), randint(1, 100))

    for method in ["timer", "gauge", "counter"]:
        for transport in ["tcp"]:
            incoming = Queue()
            server = setup_tcp_server(incoming)

            yield auto_flush, transport, method, 5, 15
            lines = []
            while 1:
                try:
                    line = incoming.get(timeout=0.1)
                    lines.append(line)
                except Empty:
                    break

            server.shutdown()
            server.server_close()
            server.thread.join()

            assert len(lines) == 15
