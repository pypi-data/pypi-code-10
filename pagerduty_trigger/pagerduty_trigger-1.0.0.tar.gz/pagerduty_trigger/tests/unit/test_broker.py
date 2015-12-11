from pagerduty.tests.unit import base
import logging

logger = logging.getLogger(__name__)


class RedisObject(object):
    def getattr(self, name):
        return None


class BrokerTest(base.BaseTest):
    def __init__(self, *args, **kwargs):
        super(BrokerTest, self).__init__(*args, **kwargs)
        from pagerduty import broker
        self.broker = broker

    def setUp(self):
        self.auto_patch('pagerduty.broker.Redis')
        self.settings = base.Settings([
            ('REDIS_SERVER', '127.0.0.1')
        ])
        self.broker.RedisClass._rconn = None
        self.broker.RedisClass._settings = None

    def tearDown(self):
        self.broker.RedisClass._rconn = None
        self.broker.RedisClass._settings = None

    def test_instantiate_broker(self):
        # verify that the call was made only one time even when instantiating twice
        self.broker.RedisClass(self.settings)
        self.broker.RedisClass(self.settings)
        self.assertTrue(self.broker.Redis.called_once)
        self.broker.Redis.assert_called_once_with(host='127.0.0.1')

    def test_instantiate_password_broker(self):
        # verify that the call was made only one time even when instantiating twice
        self.settings.REDIS_SERVER_AUTH = 'testpassword'
        self.broker.RedisClass(self.settings)
        self.assertTrue(self.broker.Redis.called_once)
        self.broker.Redis.assert_called_once_with(host='127.0.0.1', password='testpassword')

    def test_instantiated_broker(self):
        # verify that the call was made only one time even when instantiating twice
        self.broker.RedisClass._rconn = RedisObject()
        self.broker.RedisClass(self.settings)
        self.assertFalse(self.broker.Redis.called)
