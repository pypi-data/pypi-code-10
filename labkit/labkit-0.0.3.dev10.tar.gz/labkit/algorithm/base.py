#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



import abc

class BaseAlgorithm(object):
    """Base class for algorithm.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, max_width=60):
        self.max_width = max_width

    @abc.abstractmethod
    def run(self, ensemble,config):
        '''
        algorithm template, 必须实现一个run函数, 来run一个ensemble
        :param config: 传进来的配置对象
        :param config: 一个ensemble对象
        :return: ensemble
        '''
