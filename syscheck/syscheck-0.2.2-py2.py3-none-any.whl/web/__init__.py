"""Web-based interface for monitoring system statuses."""

import os.path as osp
import logging

try:
    import simplejson as json
except ImportError:
    import json

from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.options import define, options
from tornado import ioloop, gen

from ..monitor import SystemsMonitor

logger = logging.getLogger(__name__)

define('period', default=5, help='Approximate time between checks in seconds')
define('port', default=8999, help='HTTP port to serve on')
define('debug', default=False, help='Enable debug mode')
define('title', default='Systems Check', help='Page title to use')
define('url_prefix', default='', help='URL subdir')


class MainHandler(RequestHandler):
    """Main page for showing system status."""
    def initialize(self, title='Systems Check'):
        assert isinstance(title, str)
        self.title = title

    def get(self):
        self.render('index.html', title=self.title)


class StatusCheckHandler(RequestHandler):
    """AJAX status checker for clients that don't need websockets or
    don't support them.

    TODO: update to also return the checkers data

    """
    def get(self):
        self.write(CheckerApp.statuses)


class SocketHandler(WebSocketHandler):
    """Websocket connections for pushing status changes to connected
    clients.

    """
    clients = set()

    def initialize(self, checkers):
        assert isinstance(checkers, dict)
        self.checkers = checkers

    def open(self):
        SocketHandler.clients.add(self)

    def on_message(self, message):
        logger.debug('Incoming message: ' + message)
        if message == 'info?':
            self.write_message({
                'checkers': self.checkers, 'response': True, 'first': True})
        elif message == 'ping':
            self.write_message({'response': True, 'pong': None})

    @classmethod
    def push(self, statuses):
        """Push statuses to clients."""
        assert isinstance(statuses, dict)
        data = json.dumps(statuses, sort_keys=True)
        try:
            for client in self.clients:
                client.write_message(data)
        except WebSocketClosedError:
            self.clients.remove(client)


class CheckerApp(Application):
    """Tornado web app for handling status check requests."""
    statuses = None

    def __init__(self, monitor, extra_handlers=None,
                 title=options.title, *args, **kwargs):
        """Create the application.

        :param SystemsMonitor monitor: ``SystemsMonitor`` instance
        :param list extra_handlers: additional ``RequestHandler`` specs
        :param title: title for the main page

        """
        assert isinstance(monitor, SystemsMonitor)
        self.monitor = monitor
        assert isinstance(title, str)

        handlers = [
            [r'/', MainHandler, {'title': options.title}],
            [r'/status', StatusCheckHandler],
            [r'/socket', SocketHandler, {'checkers': monitor.jsonize()}]
        ]

        if options.url_prefix != '':
            prefix = options.url_prefix
            if prefix[0] != '/':
                prefix = '/' + prefix
            for handler in handlers:
                handler[0] = prefix + handler[0]
                if len(handler[0]) > 1:
                    handler[0].strip('/')

        if extra_handlers:
            handlers += extra_handlers

        self.started = False

        dirname = osp.dirname(__file__)
        static_path = osp.abspath(osp.join(dirname, 'static'))
        template_path = osp.abspath(osp.join(dirname, 'templates'))

        super(CheckerApp, self).__init__(
            handlers, *args, debug=options.debug,
            static_path=static_path, template_path=template_path,
            **kwargs)

    @gen.coroutine
    def _check_and_push(self):
        """Check all statuses and push the results with a
        websocket.

        """
        logger.debug('Checking statuses...')
        statuses = yield self.monitor.check()
        CheckerApp.statuses = {
            self.monitor.checkers[key]['name']: statuses[i] for i, key in enumerate(self.monitor.checkers.keys())}
        SocketHandler.push(self.statuses)

    def start_checking(self, period=options.period):
        """Initialize checking all checkers. This method is called
        automatically if using ``app.listen(port)`` to start the
        app. It only needs to be explicitly called if running through
        a specially configured ``HTTPServer`` instance.

        """
        callback = ioloop.PeriodicCallback(self._check_and_push, period*1000)
        callback.start()
        self.started = True

    def listen(self, port, address='', **kwargs):
        """Start listening on the given port."""
        if not self.started:
            self.start_checking()
        super(CheckerApp, self).listen(port, address, **kwargs)
