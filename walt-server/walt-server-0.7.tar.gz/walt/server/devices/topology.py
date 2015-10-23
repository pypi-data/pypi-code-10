#!/usr/bin/env python

from walt.common.tools import get_mac_address
from walt.common.nodetypes import get_node_type_from_mac_address
from walt.server.network.tools import ip_in_walt_network, lldp_update
from walt.server.tools import format_paragraph, columnate
from walt.server.tree import Tree
from walt.server import snmp, const
import time, re

TOPOLOGY_QUERY = """
    SELECT  d1.name as name, d1.type as type, d1.mac as mac,
            d1.ip as ip,
            (case when d1.reachable = 1 then 'yes' else 'NO' end) as reachable,
            d2.name as switch_name, t.switch_port as switch_port
    FROM devices d1, devices d2, topology t
    WHERE   d1.mac = t.mac and d2.mac = t.switch_mac
    UNION ALL
    SELECT  d1.name as name, d1.type as type, d1.mac as mac,
            d1.ip as ip,
            (case when d1.reachable = 1 then 'yes' else 'NO' end) as reachable,
            NULL as switch_name, NULL as switch_port
    FROM devices d1, topology t
    WHERE   d1.mac = t.mac and t.switch_mac is null
    ORDER BY switch_name, switch_port;"""

REPLACED_DEVICES_QUERY = """
    SELECT  d1.name as name, d1.type as type, d1.mac as mac,
            d1.ip as ip
    FROM devices d1 LEFT JOIN topology t
    ON   d1.mac = t.mac
    WHERE t.mac is NULL;"""

MSG_DEVICE_TREE_EXPLAIN_UNREACHABLE = """\
note: devices marked with parentheses are unreachable
"""

MSG_DEVICE_TREE_MORE_DETAILS = """
tips:
- use 'walt device rescan' to update
- use 'walt device show' for more info
"""

TITLE_DEVICE_SHOW_MAIN = """\
The WalT network contains the following devices:"""

FOOTNOTE_DEVICE_SHOW_MAIN = """\
tips:
- use 'walt device tree' for a tree view of the network
- use 'walt device rescan' to update
- use 'walt device forget <device_name>' in case of a broken device"""

TITLE_DEVICE_SHOW_REPLACED = """\
The following devices seem to have been replaced:"""

FOOTNOTE_DEVICE_SHOW_REPLACED = """\
(tip: walt device forget <device_name>)"""

class Topology(object):

    def __init__(self, db):
        self.db = db

    def get_type(self, mac):
        node_type = get_node_type_from_mac_address(mac)
        if node_type != None:
            # this is a node
            return node_type.SHORT_NAME
        elif mac == self.server_mac:
            return 'server'
        else:
            return 'switch'

    def collect_connected_devices(self, host, host_is_a_switch,
                            host_mac, processed_switches):

        print "collect devices connected on %s" % host
        # avoid to loop forever...
        if host_is_a_switch:
            processed_switches.add(host_mac)
        while True:
            issue = False
            # get a SNMP proxy with LLDP feature
            snmp_proxy = snmp.Proxy(host, lldp=True)

            # record neighbors in db and recurse
            for port, neighbor_info in snmp_proxy.lldp.get_neighbors().items():
                ip, mac = neighbor_info['ip'], neighbor_info['mac']
                if mac in processed_switches:
                    continue
                if not ip_in_walt_network(ip):
                    print 'Not ready, one neighbor has ip %s (not in WalT network yet)...' % ip
                    lldp_update()
                    time.sleep(1)
                    issue = True
                    break
                device_type = self.get_type(mac)
                if host_is_a_switch:
                    switch_mac, switch_port = host_mac, port
                else:
                    switch_mac, switch_port = None, None
                self.add_device(type=device_type,
                                mac=mac,
                                switch_mac=switch_mac,
                                switch_port=switch_port,
                                ip=ip)
                if device_type == 'switch':
                    # recursively discover devices connected to this switch
                    self.collect_connected_devices(ip, True,
                                            mac, processed_switches)
            if not issue:
                break   # otherwise restart the loop

    def rescan(self, requester=None):
        self.db.execute("""
            UPDATE devices
            SET reachable = 0;""")

        self.server_mac = get_mac_address(const.SERVER_TESTBED_INTERFACE)
        self.collect_connected_devices("localhost", False, self.server_mac, set())
        self.db.commit()

        if requester != None:
            requester.stdout.write('done.\n')

    def generate_device_name(self, **kwargs):
        if kwargs['type'] == 'server':
            return 'walt-server'
        return "%s-%s" %(
            kwargs['type'],
            "".join(kwargs['mac'].split(':')[3:]))

    def add_device(self, **kwargs):
        # if we are there then we can reach this device
        kwargs['reachable'] = 1
        # update device info
        num_rows = self.db.update("devices", 'mac', **kwargs)
        # if no row was updated, this is a new device
        if num_rows == 0:
            # generate a name for this device
            name = self.generate_device_name(**kwargs)
            kwargs['name'] = name
            # insert a new row
            self.db.insert("devices", **kwargs)
        if 'switch_mac' in kwargs:
            mac = kwargs['mac']
            switch_mac = kwargs['switch_mac']
            switch_port = kwargs['switch_port']
            # add/update topology info:
            # - update or insert topology info for device with specified mac
            # - if any other device was connected at this place, it will
            #   be replaced (thus this other device will appear disconnected)
            self.db.delete('topology', mac = mac)
            self.db.delete('topology', switch_mac = switch_mac,
                                       switch_port = switch_port)
            self.db.insert("topology", **kwargs)

    def tree(self):
        t = Tree()
        unreachable_found = False
        for device in self.db.execute(TOPOLOGY_QUERY).fetchall():
            name = device.name
            if device.reachable == 'NO':
                unreachable_found = True
                name = '(%s)' % name
            swport = device.switch_port
            if swport == None:
                label = name
                # align to 2nd letter of the name
                subtree_offset = 1
            else:
                label = '%d: %s' % (swport, name)
                # align to 2nd letter of the name
                subtree_offset = label.find(' ') + 2
            parent_key = device.switch_name
            t.add_node( name,   # will be the key in the tree
                        label,
                        subtree_offset=subtree_offset,
                        parent_key = parent_key)
        note = MSG_DEVICE_TREE_MORE_DETAILS
        if unreachable_found:
            note += MSG_DEVICE_TREE_EXPLAIN_UNREACHABLE
        return "\n%s%s" % (t.printed(), note)

    def show(self):
        # ** message about connected devices
        msg = format_paragraph(
                TITLE_DEVICE_SHOW_MAIN,
                self.db.pretty_printed_select(TOPOLOGY_QUERY),
                FOOTNOTE_DEVICE_SHOW_MAIN)
        # ** message about replaced devices, if at least one
        res = self.db.execute(REPLACED_DEVICES_QUERY).fetchall()
        if len(res) > 0:
            msg += format_paragraph(
                        TITLE_DEVICE_SHOW_REPLACED,
                        self.db.pretty_printed_resultset(res),
                        FOOTNOTE_DEVICE_SHOW_REPLACED)
        return msg

    def setpower(self, device_mac, poweron):
        switch_ip, switch_port = self.get_connectivity_info(device_mac)
        if not switch_ip:
            return False
        proxy = snmp.Proxy(switch_ip, poe=True)
        proxy.poe.set_port(switch_port, poweron)
        return True

    def get_connectivity_info(self, device_mac):
        topology_info = self.db.select_unique("topology", mac=device_mac)
        if not topology_info:
            return (None, None)
        switch_mac = topology_info.switch_mac
        switch_port = topology_info.switch_port
        switch_info = self.db.select_unique("devices", mac=switch_mac)
        return switch_info.ip, switch_port
