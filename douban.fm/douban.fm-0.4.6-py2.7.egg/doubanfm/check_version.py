#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import xmlrpclib
import pip

def is_latest(package_name):
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    for dist in pip.get_installed_distributions():
        if dist.project_name == package_name:
            available = pypi.package_releases(dist.project_name)
            if available[0] != dist.version:
                return False
            return True

def update_package(package_name):
    pip.main(['install', package_name, '--upgrade'])
