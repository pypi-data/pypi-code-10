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


def exec_service(service_command):
    subprocess.call(service_command, shell=True)


def get_connection(websocket_uri):
    try:
        return create_connection(websocket_uri)
    except socket.error as e:
        print 'Connect GLB Server failed: %r' % e
        sys.exit(1)


class Process(Daemon):

    def __init__(self, websocket_uri, s_type, pid_dist,
                 s_command, conf_dist, ssl_dist):
        super(Process, self).__init__(
            '%s%s' % (pid_dist, 'daemon-glb-slave.pid'))
        self.s_type = s_type
        self.pid_dist = pid_dist
        self.s_command = s_command
        self.conf_dist = conf_dist
        self.ssl_dist = ssl_dist
        self.conn = get_connection(websocket_uri)
        #self._run()

    def write_ssl_files(self, ssl_files):
        if self.s_type == "haproxy":
            for fname, private_key, certificate_chain in ssl_files:
                fname = "%s_%s" % (fname, 'chain.pem')
                fcontent = "\n".join([private_key, certificate_chain])
                write("%s%s" % (self.ssl_dist, fname), fcontent)
        else:
            for ssl_file in ssl_files:
                ssl_certificate = ssl_file['certificate_chain']
                ssl_certificate_key = ssl_file['private_key']
                write("%s%s" % (self.ssl_dist,
                                "%s.chained.crt" % ssl_file['name']),
                      ssl_certificate)
                write("%s%s" % (self.ssl_dist,
                                "%s.key" % ssl_file['name']),
                      ssl_certificate_key)

    def run_with_service(self, val):
        self.write_ssl_files(getattr(val, 'ssl_files', list()))
        write(self.conf_dist, val.get('conf', ''))
        exec_service(self.s_command)

    def _run(self):
        slave_version = read('%s%s' % (self.pid_dist, 'slave_version'))
        data = json.dumps(dict(addr=get_local_address(),
                               slave_version=slave_version,
                               service_type=self.s_type))
        self.conn.send(data)
        while True:
            rev_data = self.conn.recv()
            if rev_data:
                data = json.loads(rev_data)
                slave_version = data.get('slave_version', None)
                haproxy = data.get('haproxy', None)
                nginx = data.get('nginx', None)

                if slave_version is not None:
                    write('%s%s' % (self.pid_dist, 'slave_version'),
                          slave_version)
                if haproxy:
                    self.run_with_service(haproxy)
                if nginx:
                    self.run_with_service(nginx)

    def stop(self):
        self.conn.close()
        super(Process, self).stop()
