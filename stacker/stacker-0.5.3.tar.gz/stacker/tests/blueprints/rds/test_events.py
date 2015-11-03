import unittest
import json

from stacker.blueprints.rds.events import EventSubscriptions
from stacker.context import Context


class TestEventSubscriptions(unittest.TestCase):
    def test_fail_no_sourceids(self):
        c = Context(
            {"environment": "test", "namespace": "test-namespace"},
            parameters={
                "SourceIds": "my-db1,my-db2",
                "Subscriptions": [("http", "http://my.test.endpoint.com")],
            }
        )
        bp = EventSubscriptions("test", c)
        json.loads(bp.rendered)
