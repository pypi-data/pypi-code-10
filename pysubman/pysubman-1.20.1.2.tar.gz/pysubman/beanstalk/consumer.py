#!/usr/bin/env python
# coding=utf-8

"""
消费者
"""

from .connection import Connection
from .constants import DEFAULT_ADDRESS, ConsumerException
from .service import Service
from .tube import Tube


class Consumer(object):
    def __init__(self, address=DEFAULT_ADDRESS, services=None, use_threading=False):
        """ new consumer

        :param string address: beanstalk address
        :param services: 监听的服务
        :type services: `~pysubman.service.Service`
        :param bool use_threading: 是否开启多线程
        """

        if (services is None
                or not isinstance(services, Service)
                or not services.get_all_services()):
            raise ConsumerException("services not empty")

        self.services = services
        self.address = address
        self.connection = Connection(self.address)
        self.use_threading = use_threading

    def tube(self, tube):
        """ 监听 tube

        :param string tube: beanstalk tube name

        :rtype: `~pysubman.threadtube.ThreadTube` or `~pysubman.tube.Tube`
        :return: return tube handler
        """

        if self.use_threading:
            from .threadtube import ThreadTube
            return ThreadTube(self, tube)
        return Tube(self, tube)
