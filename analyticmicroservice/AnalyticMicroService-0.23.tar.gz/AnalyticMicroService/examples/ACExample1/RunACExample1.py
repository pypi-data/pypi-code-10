__author__ = 'Chris Bergh'
import subprocess
import sys
import json
sys.path.insert(0, '../../../../AnalyticMicroService')
import argparse
from collections import OrderedDict
from AnalyticMicroService.server.utils.AMSSingletons import AMSLogger
from contextlib import contextmanager
import signal
from docker import Client, errors, utils
from docker.errors import APIError
AC1_DATA_CONTAINER_NAME = 'data-container-name'
AC1_DATA_CONTAINER_PATH = 'data-container-path'
AC1_CONTAINER_NAME = 'container-name'
AC1_IMAGE_REPO = 'image-repo'
AC1_IMAGE_TAG = 'image-tag'

# note: bastardized version of AMSCommandRunner.py
class ACExample1Runner(object):

    def __init__(self, ac1_config):
        self.config = ac1_config
        self.docker_base_url='unix://var/run/docker.sock'
        self.docker_client = Client(base_url=self.docker_base_url)
        self.container = None
        self.container_name = self.config.get(AC1_CONTAINER_NAME)
        self.data_container = None
        self.data_container_name = self.config.get(AC1_DATA_CONTAINER_NAME)
        self.image_repository = self.config.get(AC1_IMAGE_REPO)
        self.image_tag = self.config.get(AC1_IMAGE_TAG)

    def images(self):
        the_images = self.docker_client.images()
        return the_images

    # docker rm $(docker ps -a -q)
    @staticmethod
    def cleanup_all():
        p=None
        try:
            contianer_list_cmd = "docker ps -a -q"
            if len(subprocess.Popen(contianer_list_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()) > 0:
                contianer_rm_cmd = "docker rm $(docker ps -a -q)"
                p = subprocess.Popen(contianer_rm_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        except Exception, e:
            return "ERROR"
        return p

    # sudo docker build -t ac_container_example1 .
    def build(self, build_path=".", no_cache=False):
        try:
            response = [line for line in (self.docker_client.build(path=build_path, tag=self.container_name, nocache=no_cache))]
        except TypeError, t:
            return None
        return response

    def image_exists(self):
        image_list = self.images()
        the_image = None
        for image in image_list:
            if 'RepoTags' in image and isinstance(image['RepoTags'], list):
                for tag in image['RepoTags']:
                    if tag == self.image_repository + ":" + self.image_tag:
                        the_image = image
        if the_image is None:
            return False
        else:
            return True

    def create_container(self):
        image_name = '%s:%s' % (self.image_repository, self.image_tag)
        try:
            container = self.docker_client.create_container(image_name)
        except  APIError, e:
            return None

        return container

    #starts a container
    #  sudo docker run -e AC_FILE_MOUNT="/ACExample1/docker-share" --volumes-from data-ac-example1 ac_container_example1:latest
    def start_container(self, environment_dict, volumes_from_str):
        if isinstance(environment_dict, dict) is False or isinstance(volumes_from_str, str) is False:
            return False

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
        if self.image_exists() is False:
            self.build()
        image_name = '%s:%s' % (self.image_repository, self.image_tag)
        try:
            self.container = self.docker_client.create_container(image=image_name, environment=environment_dict )
        except  APIError, e:
            return False

        if self.container is None:
            return False
        try:
            self.docker_client.start(self.container.get('Id'), volumes_from=volumes_from_str)
            info =  self.docker_client.inspect_container(self.container)
        except Exception, e:
            return False
        out = ''
        try:
            with time_limit(2):
                for line in self.docker_client.logs(self.container, stderr=False, stream=True):
                    out += line
        except TimeoutException:
            pass
        return True

    # starts a data container and copies a config file into the shared volume
    # create data container:    sudo docker run -d -v /ACExample1/docker-share --name="data-ac-example1" ac_container_example1:latest
    # add config file:          sudo docker cp docker-share/config.json data-ac-example1:/ACExample1/docker-share/config.json
    def start_data_container(self, dc_name, volume_location, in_config_file_path, dc_config_file_path):
        # does the container already exist on this machine?
        if self.image_exists() is False:
            self.build()
        image_name = '%s:%s' % (self.image_repository, self.image_tag)
        try:
            self.data_container = self.docker_client.create_container(image=image_name, detach=True, name=dc_name, volumes=volume_location)
        except  APIError, e:
            return False

        if self.data_container is None:
            return False

        try:
            p = subprocess.call(['docker', 'cp', in_config_file_path, dc_config_file_path])
            if p < 0:
                return False
        except Exception, e:
            return False
        # depricated
        # if self.docker_client.copy(in_config_file_path, dc_config_file_path) is False:
        #     return False
        return True


    def stop_container(self):
        if self.docker_client is not None:
            if self.container is not None:
                try:
                    self.docker_client.kill(self.container)
                except APIError:
                    self.docker_client.wait(self.container)
                try:
                    self.docker_client.remove_container(self.container)
                except APIError:
                    pass
            if self.data_container is not None:
                try:
                    self.docker_client.kill(self.data_container)
                except APIError:
                    self.docker_client.wait(self.data_container)
                try:
                    self.docker_client.remove_container(self.data_container)
                except APIError:
                    pass

    # same as docker ps -f="image=cbergh"
    def force_remove_container(self):
        cf = dict()
        cf['Image'] = '%s:%s' % (self.image_repository, self.image_tag)
        try:
            the_container =  self.docker_client.containers(filters=cf)
        except APIError:
            return False
        if the_container is None or isinstance(the_container, list) is False \
                or len(the_container) != 1 or isinstance(the_container[0], dict) is False \
                or "Id" not in the_container[0]:
            return False
        try:
            self.docker_client.remove_container(the_container[0]['Id'], force=True)
        except APIError:
            return False
        return True


def main(parser=None):
    share_dir = 'docker-share'
    config_file = 'config.json'
    config_dict = dict()
    config_dict[AC1_CONTAINER_NAME] = 'ac_container_example1'
    config_dict[AC1_DATA_CONTAINER_NAME] = 'data-ac-example1'
    config_dict[AC1_DATA_CONTAINER_PATH] = '/ACExample1/%s' % share_dir
    config_dict[AC1_IMAGE_REPO] = 'ac_container_example1'
    config_dict[AC1_IMAGE_TAG] = 'latest'
    env_dict = {"AC_FILE_MOUNT": config_dict[AC1_DATA_CONTAINER_PATH]}

    ac_runner = ACExample1Runner(config_dict)
    cleanup_str = ac_runner.cleanup_all()
    if cleanup_str is not None:
        print cleanup_str

    if ac_runner.image_exists() is False:
        print '...RunACExample1: building image (may take a while)'
        br = ac_runner.build(".", False)
        print br

    images = ac_runner.images()
    if len(images) == 0:
        AMSLogger.log_and_print_error('...RunACExample1:  failed to find images , exiting')
    else:
        if ac_runner.start_data_container(config_dict[AC1_DATA_CONTAINER_NAME],
                                          config_dict[AC1_DATA_CONTAINER_PATH],
                                          '%s/%s' % (share_dir, config_file),
                                          '%s:%s/%s' % (config_dict[AC1_DATA_CONTAINER_NAME], config_dict[AC1_DATA_CONTAINER_PATH], config_file)) is False:
            AMSLogger.log_and_print_error('...RunACExample1:  failed to create data container, exiting')
        else:
            if ac_runner.start_container(env_dict, config_dict[AC1_DATA_CONTAINER_NAME]) is False:
                AMSLogger.log_and_print_error('...RunACExample1:  failed to run container, exiting')
            else:
                #see in data container:    sudo ls -al `docker inspect --format='{{(index .Mounts 0).Source}}' data-ac-example1`
                cmd = "sudo ls -al `docker inspect --format='{{(index .Mounts 0).Source}}' %s`" % config_dict[AC1_DATA_CONTAINER_NAME]
                print "...RunACExample1:  here are the files in the data container:"
                print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
                AMSLogger.log_and_print('...RunACExample1:  Completed command, exiting')

    ac_runner.stop_container()

if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser(description="Welcome to the RunACExample1 Program")
    main(cmdline_parser)
