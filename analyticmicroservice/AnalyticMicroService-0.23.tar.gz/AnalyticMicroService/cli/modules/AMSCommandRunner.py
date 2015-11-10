__author__ = 'Chris Bergh'

import requests
from contextlib import contextmanager
import signal
from collections import OrderedDict
from requests import RequestException
from docker import Client, errors, utils
from docker.errors import APIError
from AMSCommandRunnerConfig import *

class AMSCommandRunner(object):

    def __init__(self, ams_config):
        self._config = ams_config
        self._docker_base_url='unix://var/run/docker.sock'
        self._docker_client = Client(base_url=self._docker_base_url)
        self._container = None
        self._ams_url = self._config.get(AMS_URL)
        self._ams_port = self._config.get(AMS_PORT)
        self._container_name = self._config.get(AMS_CONTAINER_NAME)
        self._image_repository = self._config.get(AMS_IMAGE_REPO)
        self._image_tag = self._config.get(AMD_IMAGE_TAG)
        self._host_port = -1


    @staticmethod
    def rude():
        return '**rude**'

    def get_host_port(self):
        return self._host_port

    def images(self):
        the_images = self._docker_client.images()
        return the_images

    def search(self, search_string):
        sr = self._docker_client.search(search_string)
        return sr

    def pull(self):
        ir = self._docker_client.pull(self._image_repository, self._image_tag)
        if ir is None or isinstance(ir, basestring) is False:
            return None
        else:
            irs = ir.split('\r\n')
            out_list = list()
            for s in irs:
                if len(s) > 1:
                    rv = OrderedDict()
                    try:
                        rv = json.loads(s,  object_pairs_hook=OrderedDict)
                    except ValueError, v:
                        pass
                    out_list.append(rv)
        return out_list

    def create_container(self):
        image_name = '%s:%s' % (self._image_repository, self._image_tag)
        try:
            container = self._docker_client.create_container(
                image_name,
                ports=[(self._ams_port, 'tcp')])
        except  APIError, e:
            return None

        return container

    #from http://blog.bordage.pro/avoid-docker-py/
    def start_container(self):
        class TimeoutException(Exception):
            pass

        @contextmanager
        def time_limit(seconds):  # From http://stackoverflow.com/a/601168/1576438
            def signal_handler(signum, frame):
                raise TimeoutException('Timed out!')
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(seconds)
            try:
                yield
            finally:
                signal.alarm(0)

        # does the container already exist on this machine?
        image_list = self.images()
        the_image = None
        for image in image_list:
            if 'RepoTags' in image and isinstance(image['RepoTags'], list):
                for tag in image['RepoTags']:
                    if tag == self._image_repository + ":" + self._image_tag:
                        the_image = image
        if the_image is None:
            self.pull()
        self._container = self.create_container()

        if self._container is None:
            return False
        port_bind = dict()
        port_bind[self._ams_port] = list()
        port_bind[self._ams_port].append('0.0.0.0')
        port_bind[self._ams_port].append(self._ams_port)

        #http://stackoverflow.com/questions/21112651/how-to-run-basic-web-app-container-in-docker-py
        try:
            self._docker_client.start(self._container.get('Id'), publish_all_ports=True)
            info =  self._docker_client.inspect_container(self._container)
            self._host_port = str(info['NetworkSettings']['Ports'][self._ams_port + '/tcp'][0]['HostPort'])
        except Exception, e:
            return False
        out = ''
        try:
            with time_limit(2):
                for line in self._docker_client.logs(self._container, stderr=False, stream=True):
                    out += line
        except TimeoutException:
            pass
        return True

    def stop_container(self):
        if self._docker_client is not None and self._container is not None:
            try:
                self._docker_client.kill(self._container)
            except APIError:
                self._docker_client.wait(self._container)
            try:
                self._docker_client.remove_container(self._container)
            except APIError:
                return False
            return True
        else:
            return False
    # same as docker ps -f="image=cbergh"

    def force_remove_container(self):
        cf = dict()
        cf['Image'] = '%s:%s' % (self._image_repository, self._image_tag)
        try:
            the_container =  self._docker_client.containers(filters=cf)
        except APIError:
            return False
        if the_container is None or isinstance(the_container, list) is False \
                or len(the_container) != 1 or isinstance(the_container[0], dict) is False \
                or "Id" not in the_container[0]:
            return False
        try:
            self._docker_client.remove_container(the_container[0]['Id'], force=True)
        except APIError:
            return False
        return True


