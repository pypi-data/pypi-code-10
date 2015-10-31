#!/usr/bin/env python
from __future__ import division

import logging
from socket import socket,getaddrinfo,AF_UNSPEC,SOCK_STREAM,gaierror, \
        error as socket_error,timeout as timeout_error
from time import time

class ConnectTimePlugin(object):
    name = "connect-time"
    collectd_name = "collectd_connect_time"

    def __init__(self,collectd=None):
        self.target = []
        self.collectd = collectd
        self.interval = 10

    def collectd_configure(self,config):
        self.info("configuring")
        for node in config.children:
            k = node.key.lower()
            if  k == "target":
                self.target = node.values
            elif k == "interval":
                self.interval = int(node.values[0])
            else:
                collectd.warn("Unknown config option: {}".format(key))

        self.info("Configured with {}".format(self.target))
        self.collectd.register_read(self.collectd_read,self.interval,name=self.collectd_name)
        if not self.target:
            self.error("no target set, bailing out")
            self.collectd.unregister_read(self.read)

    def collectd_read(self):
        def to_us(t):
            return int(round(t * 1000 * 1000,0))

        if not self.target:
            self.error("read: no target set")
        for t in self.target:
            target_val = self.get_target_val(t)

            # dispatch resolve time
            if target_val['resolve']:
                val = self.collectd.Values(plugin=self.name)
                val.type = 'response_time'
                val.type_instance = 'resolve'
                val.plugin_instance = t
                val.values = [to_us(target_val['resolve'])]
                val.dispatch()
            else:
                self.error('resolve time is None for {}'.format(t))
                continue
            # dispatch min,max,avg
            for ti in ("max","min","avg"):
                val = self.collectd.Values(plugin=self.name)
                val.type = 'response_time'
                val.type_instance = ti
                val.plugin_instance = t
                try:
                    val.values = [to_us(target_val['collect'][ti])]
                    val.dispatch()
                except ValueError as e:
                    self.error("cannot dispatch value for target {} -> {}".format(t,e))

    def get_target_val(self,t):
        try:
            host,port = t.split(":")
            port = int(port)
        except ValueError:
            self.debug("defaulting for {} to port 80".format(t))
            host = t
            port = 80
        ret = { 'host': host,
                'port': port,
                'resolve': None,
                'raw' : {},
                'collect': {
                    'min':None,
                    'max':None,
                    'avg':None
                    }
        }
        try:
            begin = time()
            ai = getaddrinfo(host,port,AF_UNSPEC,SOCK_STREAM)
            ret['resolve'] =  (time() - begin)
        except gaierror as e:
            self.error("Cannot resolve {}".format(e))
        else:
            for fam,typ,proto,canon,addr in ai:
                try:
                    begin = time()
                    s = socket(fam,typ)
                    s.settimeout(5)
                    s.connect(addr)
                    # microSeconds
                    duration = (time() - begin)
                except socket_error as e:
                    self.debug("{} -> {}".format(addr[0],e))
                except timeout_error as e:
                    self.error("{} - Timeout error!".format(addr[0],e))
                    # 5 seconds
                    duration = 5
                else:
                    k = "{}:{}".format(*addr)
                    # time in uS
                    ret['raw'][k] = duration

        vals = ret['raw'].values()
        if vals:
            ret['collect']['max'] = max(vals)
            ret['collect']['min'] = min(vals)
            ret['collect']['avg'] = sum(vals) / len(vals)
        return ret

    def debug(self,msg):
        if self.collectd: self.collectd.debug(msg)
        else: logging.debug(msg)

    def error(self,msg):
        if self.collectd: self.collectd.error(msg)
        else: logging.error(msg)

    def info(self,msg):
        if self.collectd: self.collectd.info(msg)
        else: logging.info(msg)

def cli():
    import sys,json
    from json import encoder
    # Change the json decoder for FLOAT, change Seconds to ms
    encoder.FLOAT_REPR = lambda o: format(o*1000, '.2f')
    if len(sys.argv) < 2:
        print("usage: {} HOSTNAME".format(sys.argv[0].split('/')[-1]))
        sys.exit(1)
    c = ConnectTimePlugin().get_target_val(sys.argv[1])

    print(json.dumps(c,indent=4))

def run_collectd(collectd):
    c = ConnectTimePlugin(collectd)
    collectd.register_config(c.collectd_configure,name="collectd_connect_time")

if __name__ == "__main__":
    cli()

