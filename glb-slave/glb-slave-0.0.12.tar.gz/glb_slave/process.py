# -*- coding: utf-8 -*-
import re
import sys
import json
import codecs
import socket
import subprocess
from websocket import create_connection
from subprocess import Popen, PIPE
from os import makedirs
from os.path import exists, dirname
from .daemon import Daemon


def write(dist, content):
    dir_ = dirname(dist)
    if not exists(dir_):
        makedirs(dir_)
    with codecs.open(dist, 'w', 'utf-8') as f:
        f.write(content)


def read(dist):
    if not exists(dist):
        return
    with codecs.open(dist, 'r', 'utf-8') as f:
        return f.readline()


def get_local_address():
    return re.search('\d+\.\d+\.\d+\.\d+',
                     Popen('ifconfig', stdout=PIPE).stdout.read()).group(0)


def update_service_config(path, content):
    write(path, content)


def reload_service(service_path):
    subprocess.call('%s reload' % service_path, shell=True)


class Process(Daemon):

    def __init__(self, websocket, pid_dist, nginx_switch,
                 haproxy_cfg_dist, haproxy_service_dist, haproxy_ssl_dist,
                 nginx_conf_dist, nginx_service_dist, nginx_ssl_dist):
        super(Process, self).__init__(
            '%s%s' % (pid_dist, 'daemon-glb-slave.pid'))
        self.websocket = websocket
        self.nginx_switch = nginx_switch
        self.pid_dist = pid_dist
        self.haproxy_cfg_dist = haproxy_cfg_dist
        self.haproxy_service_dist = haproxy_service_dist
        self.haproxy_ssl_dist = haproxy_ssl_dist

        self.nginx_conf_dist = nginx_conf_dist
        self.nginx_service_dist = nginx_service_dist
        self.nginx_ssl_dist = nginx_ssl_dist
        self.conn = self._get_connection()
        #self._run()

    def _get_connection(self):
        try:
            return create_connection(self.websocket)
        except socket.error as e:
            print 'Connection failed: %r' % e
            sys.exit(1)

    def _run(self):
        slave_version = read('%s%s' % (self.pid_dist, 'slave_version'))
        #print slave_version
        #slave_version = '1.0'
        data = json.dumps(dict(addr=get_local_address(),
                               slave_version=slave_version,
                               nginx_switch=self.nginx_switch))
        #print data
        self.conn.send(data)
        while True:
            #print '----' * 20
            rev_data = self.conn.recv()
            if rev_data:
                data = json.loads(rev_data)
                slave_version = data.get('slave_version', None)
                haproxy = data.get('haproxy', None)
                nginx = data.get('nginx', None)

                #print slave_version
                #print '----' * 20
                if slave_version is not None:
                    write('%s%s' % (self.pid_dist, 'slave_version'),
                          slave_version)
                if haproxy is not None:
                    self.run_with_haproxy(haproxy)
                if nginx is not None:
                    self.run_with_nginx(nginx)

    def run_with_haproxy(self, val):
        self.write_haproxy_pems(getattr(val, 'ssl_files', list()))
        update_service_config(self.haproxy_cfg_dist, val['conf'])
        reload_service(self.haproxy_service_dist)

    def run_with_nginx(self, val):
        self.write_nginx_ssl_files(getattr(val, 'ssl_files', list()))
        update_service_config(self.nginx_conf_dist, val['conf'])
        reload_service(self.nginx_service_dist)

    def stop(self):
        self.conn.close()
        super(Process, self).stop()

    def write_haproxy_pems(self, pem_files):
        for filename, private_key, certificate_chain in pem_files:
            file_name = "%s_%s" % (filename, 'chain.pem')
            file_content = "\n".join([private_key, certificate_chain])
            write("%s%s" % (self.haproxy_ssl_dist, file_name), file_content)

    def write_nginx_ssl_files(self, ssl_files):
        for ssl_file in ssl_files:
            ssl_certificate = ssl_file['certificate_chain']
            ssl_certificate_key = ssl_file['private_key']
            write("%s%s" % (self.nginx_ssl_dist,
                            "%s.chained.crt" % ssl_file['name']),
                  ssl_certificate)
            write("%s%s" % (self.nginx_ssl_dist,
                            "%s.key" % ssl_file['name']),
                  ssl_certificate_key)
