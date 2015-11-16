from OpenvSwitchClient import OpenvSwitchClient
from operations.Transaction import *
from pprint import pprint
from cygnet_common.jsonrpc.helpers.Switch import OVSwitch
from cygnet_common.jsonrpc.helpers.Port import OVSPort
from cygnet_common.jsonrpc.helpers.Interface import OVSInterface
from cygnet_common.jsonrpc.helpers.Bridge import OVSBridge
from uuid import uuid1
from cygnet_common.jsonrpc.types import *
a = OpenvSwitchClient('unix:///var/run/openvswitch/db.sock')
import OpenvSwitchTables
req_switch = OpenvSwitchTables.OpenvSwitchTable()
req_bridge = OpenvSwitchTables.BridgeTable()
req_port = OpenvSwitchTables.PortTable()
req_interface = OpenvSwitchTables.InterfaceTable()
print 'REQ:',req_switch
state = a.getState([req_switch, req_port, req_bridge,req_interface])

a.addBridge('foopytest')
a.addPort('foopytest','eth1')
a.setBridgeProperty('foopytest','stp_enable',True)
a.addPort('foopytest','gre0')
iface = a.getInterface('gre0')
options = iface.options
options.append(OVSAtom(['remote_ip','1.2.3.4']))
a.setInterfaceProperty('gre0','options',options)

#a.removePort('eth1')
#a.removeBridge('foopytest')


'''
i = OVSInterface('fooiface')
i.uuid_name = 'row'+str(uuid1())
print '\n\n\n'
for instance in state.bridges.itervalues():
    pprint(WaitTransaction(instance))
    print '-----------'
x =  InsertTransaction(i)
x.row = {'ports':{'foo':i}}
print x
#print state.ports
print ''
#print state.interfaces
'''
