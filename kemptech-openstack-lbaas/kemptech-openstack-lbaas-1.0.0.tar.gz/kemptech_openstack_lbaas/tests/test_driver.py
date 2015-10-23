import mock

from neutron_lbaas.tests.unit.db.loadbalancer import test_db_loadbalancerv2

LBAAS_PROVIDER=('LOADBALANCERV2:kemptechnologies:neutron_lbaas.services.'
                'loadbalancer.drivers.kemptechnologies.driver.'
                'KempLoadMasterDriver:default')


class TestLoadBalancerManager(test_db_loadbalancerv2):
    def test_create(self):
        self.fail()

    def test_update(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test_refresh(self):
        self.fail()

    def test_stats(self):
        self.fail()


class TestKempLoadMasterDriver(test_db_loadbalancerv2.LbaasPluginDbTestCase):
    pass
