# -*- coding: utf-8 -*-
import fakeredis
import logging
import mock
import tempfile
import unittest

import gribble
from gribble.config import GribbleConfig
from gribble.transports import create_transport
from gribble.transports.base_transport import BaseTransport

try:
    from gribble.transports.zmq_transport import ZmqTransport
    zmqSkip = False
except ImportError, e:
    if e.message == 'No module named zmq':
        zmqSkip = True
    else:
        raise

class DummyTransport(BaseTransport):
    pass


with mock.patch('pika.adapters.SelectConnection', autospec=True) as mock_pika:

    class TransportConfigTests(unittest.TestCase):
        def setUp(self):
            self.logger = logging.getLogger(__name__)

        def _get_config(self, **kwargs):
            empty_conf = tempfile.NamedTemporaryFile(delete=True)
            return GribbleConfig(mock.Mock(config=empty_conf.name, **kwargs))

        @mock.patch('pika.adapters.SelectConnection', mock_pika)
        def test_builtin_rabbitmq(self):
            gribble_config = self._get_config(transport='rabbitmq')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, gribble.transports.rabbitmq_transport.RabbitmqTransport)

        @mock.patch('redis.StrictRedis', fakeredis.FakeStrictRedis)
        def test_builtin_redis(self):
            gribble_config = self._get_config(transport='redis')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, gribble.transports.redis_transport.RedisTransport)

        def test_builtin_stdout(self):
            gribble_config = self._get_config(transport='stdout')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, gribble.transports.stdout_transport.StdoutTransport)

        def test_builtin_udp(self):
            gribble_config = self._get_config(transport='udp')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, gribble.transports.udp_transport.UdpTransport)

        @unittest.skipIf(zmqSkip, 'zmq not installed')
        def test_builtin_zmq(self):
            gribble_config = self._get_config(transport='zmq')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, ZmqTransport)

        def test_custom_transport(self):
            gribble_config = self._get_config(transport='gribble.tests.test_transport_config.DummyTransport')
            transport = create_transport(gribble_config, logger=self.logger)
            self.assertIsInstance(transport, DummyTransport)
