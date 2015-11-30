# -*- coding: utf-8 -*-
'''Init and utils.'''

from logging import getLogger
from zope.i18nmessageid import MessageFactory

PROJECT_NAME = 'redturtle.prepoverlays'
_ = MessageFactory(PROJECT_NAME)
logger = getLogger(PROJECT_NAME)


def initialize(context):
    '''Initializer called when used as a Zope 2 product.'''
