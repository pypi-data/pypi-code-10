from __future__ import absolute_import
from __future__ import unicode_literals

import os

from compose.cli import docker_client
from tests import mock
from tests import unittest


class DockerClientTestCase(unittest.TestCase):

    def test_docker_client_no_home(self):
        with mock.patch.dict(os.environ):
            del os.environ['HOME']
            docker_client.docker_client()

    def test_docker_client_with_custom_timeout(self):
        timeout = 300
        with mock.patch('compose.cli.docker_client.HTTP_TIMEOUT', 300):
            client = docker_client.docker_client()
            self.assertEqual(client.timeout, int(timeout))
