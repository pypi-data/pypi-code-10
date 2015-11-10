# -*- coding: utf-8 -*-

# windows: python setup.py install --boost-dir=../../lib/boost_1.58_win64 --event-engine-include=../../../ --event-engine-lib=../../lib/win64/
# mac: python setup.py install --boost-dir=../../lib/boost_1.58_mac --event-engine-include=../../../ --event-engine-lib=../../lib/mac/
from distutils.version import StrictVersion
from setuptools import (
    Extension,
    find_packages,
    setup,
)

module1 = {'./build/keystone/':['engine.so']}

# setup
setup (name = 'keystone_sdk',
		version = '0.0.3',
		description = 'keystone python SDK for backtesting',
        packages = find_packages('./build/'),
        data_files = [('keystone',['./build/keystone/engine.so'])])
