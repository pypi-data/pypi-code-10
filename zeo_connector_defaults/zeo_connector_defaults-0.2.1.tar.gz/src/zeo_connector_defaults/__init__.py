#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

from environment_generator import tmp_context
from environment_generator import tmp_context_name

from environment_generator import generate_environment
from environment_generator import cleanup_environment


# Functions ===================================================================
def _in_path(fn, dirname="default_data"):
    pwd = os.path.dirname(__file__)
    return os.path.join(os.path.abspath(pwd), dirname, fn)


# Variables ===================================================================
SERVER_CONF_PATH = _in_path(fn="zeo.conf", dirname="default_data")
CLIENT_CONF_PATH = _in_path(fn="zeo_client.conf", dirname="default_data")

_SERVER_CONF_PATH = _in_path(fn="zeo.conf", dirname="template_data")
_CLIENT_CONF_PATH = _in_path(fn="zeo_client.conf", dirname="template_data")
