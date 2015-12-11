# -*- coding: utf-8 -*-
"""
    tests.test_simulator
    ~~~~~~~~~~~~~~~~~~~~
    Test for Simulator
    :copyright: (c) 2014-2015 Dmitry Korobitsin <https://github.com/korobitsin>
    :license: BSD, see LICENSE
"""
import unittest
import asyncore
import time
import os
from pysnmp.entity.rfc3413.oneliner import cmdgen
from snmp_simulator import Simulator


WALK_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cisco_2801.walk'))


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator(host='127.0.0.1', port=1161, rcommunity='public')

    def tearDown(self):
        pass

    def test_add_walk_file(self):
        self.simulator.add_walkfile(WALK_FILE)

    def test_snmp_get(self):
        self.simulator.add_walkfile(WALK_FILE)

        def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
            if errorIndication or errorStatus:
                raise Exception('SNMP error!')

            oid, val = varBinds[0]
            assert oid.prettyPrint() == '1.3.6.1.2.1.1.1.0'
            assert val.prettyPrint().startswith('Cisco')

        cmdGen = cmdgen.AsynCommandGenerator()
        cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('127.0.0.1', 1161)),
            (cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0),),
            (cbFun, None)
        )
        simulator_snmpEngine = self.simulator.snmp_agent.snmpEngine
        while cmdGen.snmpEngine.transportDispatcher.jobsArePending() or cmdGen.snmpEngine.transportDispatcher.transportsAreWorking():
            asyncore.poll(0.001, cmdGen.snmpEngine.transportDispatcher.getSocketMap())
            cmdGen.snmpEngine.transportDispatcher.handleTimerTick(time.time())

            asyncore.poll(0.001, simulator_snmpEngine.transportDispatcher.getSocketMap())
            simulator_snmpEngine.transportDispatcher.handleTimerTick(time.time())


if __name__ == '__main__':
    unittest.main()
