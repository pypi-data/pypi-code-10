from pagerduty_trigger.tests.unit import base
import logging

logger = logging.getLogger(__name__)


class PagerDutyTest(base.BaseTest):
    def __init__(self, *args, **kwargs):
        super(PagerDutyTest, self).__init__(*args, **kwargs)
        import pagerduty_trigger
        self.pagerduty = pagerduty_trigger

    def setUp(self):
        self.auto_patch('pagerduty_trigger.broker.Redis')
        self.pygerduty = self.auto_patch('pagerduty_trigger.pygerduty.PagerDuty')
        self.pagerduty.Pager.pager = None
        self.settings = base.Settings([
            ('PAGERDUTY_SERVICE_KEY', 'pagerdutykey'),
            ('PAGERDUTY_SUBDOMAIN', 'integrations'),
            ('REDIS_SERVER', '127.0.0.1')
        ])

    def test_instantiate_pagerduty(self):
        # verify that the call was made only one time even when instantiating twice
        self.pagerduty.Pager(self.settings)
        self.pagerduty.Pager(self.settings)
        self.assertTrue(self.pygerduty.called)
        self.pygerduty.called_once_with('cloudintegration', 'junk')

    def test_trigger_incident(self):
        self.pager = self.pagerduty.Pager(self.settings)
        args = ('pagerdutykey', 'test', 'trigger', None, 'test/error')
        kwargs = {'client_url': None, 'client': None}
        self.pager.trigger_incident('test', 'test/error')
        self.pygerduty.return_value.trigger_incident.assert_called_with(*args, **kwargs)

    def test_trigger_incident_exception(self):
        self.pygerduty.return_value.trigger_incident.side_effect = Exception('testexception')
        self.pager = self.pagerduty.Pager(self.settings)
        args = ('pagerdutykey', 'test', 'trigger', None, 'test/error')
        kwargs = {'client_url': None, 'client': None}
        with self.assertRaises(Exception) as exc:
            self.pager.trigger_incident('test', 'test/error')
        self.pygerduty.return_value.trigger_incident.assert_called_with(*args, **kwargs)
        self.assertEquals('testexception', exc.exception.message)

    def test_trigger_incident_no_service_key(self):
        self.settings.PAGERDUTY_SERVICE_KEY = None
        self.pager = self.pagerduty.Pager(self.settings)
        resp = self.pager.trigger_incident('test', 'test/error')
        self.assertIsNone(resp)

    def test_trigger_incident_redis_locked(self):
        self.auto_patch('pagerduty_trigger.IncidentKeyLock._rconn')
        self.pagerduty.IncidentKeyLock._rconn.set.return_value = None
        self.pager = self.pagerduty.Pager(self.settings)
        resp = self.pager.trigger_incident('test', 'test/error')
        self.assertIsNone(resp)
