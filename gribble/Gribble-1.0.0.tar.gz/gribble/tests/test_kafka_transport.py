# -*- coding: utf-8 -*-
import mock
import unittest
import tempfile
import logging

from kafka import KafkaClient, MultiProcessConsumer

import gribble
from gribble.config import GribbleConfig
from gribble.transports import create_transport

from gribble.unicode_dammit import unicode_dammit

from fixtures import Fixture, ZookeeperFixture, KafkaFixture

try:
    from gribble.transports.kafka_transport import KafkaTransport
    skip = False
except ImportError, e:
    if e.message == 'No module named kafka':
        skip = True
    else:
        raise


@unittest.skipIf(skip, 'kafka not installed')
class KafkaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)

        empty_conf = tempfile.NamedTemporaryFile(delete=True)
        cls.gribble_config = GribbleConfig(mock.Mock(config=empty_conf.name))

        output_file = Fixture.download_official_distribution()
        Fixture.extract_distribution(output_file)
        cls.zk = ZookeeperFixture.instance()
        cls.server = KafkaFixture.instance(0, cls.zk.host, cls.zk.port)

    @classmethod
    def tearDownClass(cls):
        cls.server.close()
        cls.zk.close()

    def test_builtin_kafka(cls):
        cls.gribble_config.set('transport', 'kafka')
        cls.gribble_config.set('logstash_version', 1)
        cls.gribble_config.set('kafka_hosts', cls.server.host + ":" + str(cls.server.port))

        transport = create_transport(cls.gribble_config, logger=cls.logger)

        cls.assertIsInstance(transport, gribble.transports.kafka_transport.KafkaTransport)

        data = {}
        lines = []
        n=100
        for i in range(n):
            lines.append('log' + str(i) + '\n')
        new_lines = []
        for line in lines:
            message = unicode_dammit(line)
            if len(message) == 0:
                continue
            new_lines.append(message)
        data['lines'] = new_lines
        data['fields'] = []
        transport.callback("test.log", **data)

        messages = cls._consume_messages(cls.server.host, cls.server.port)
        cls.assertEqual(n, messages.__len__())
        for message in messages:
            cls.assertIn('"file": "test.log", "message": "log', message.message.value);
            print(message)
        print('\n')

        transport.interrupt()

    def _consume_messages(cls, host, port):
        kafka = KafkaClient(cls.server.host + ":" + str(cls.server.port))
        consumer = MultiProcessConsumer(kafka, None, cls.gribble_config.get('kafka_topic'), num_procs=5)
        return consumer.get_messages(count=100, block=True, timeout=5)

