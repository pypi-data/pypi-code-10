# -*- coding: utf-8 -*-
u"""
Created on 2015-9-17

@author: cheng.li
"""

import sys
import io
from setuptools import setup

if sys.version_info > (3, 0, 0):
    requirements = "requirements/py3.txt"
else:
    requirements = "requirements/py2.txt"

setup(
    name='AlgoTrading',
    version='0.1.0',
    url='',
    packages=['AlgoTrading',
              'AlgoTrading.Assets',
              'AlgoTrading.Backtest',
              'AlgoTrading.Data',
              'AlgoTrading.Data.DataProviders',
              'AlgoTrading.Events',
              'AlgoTrading.Execution',
              'AlgoTrading.Finance',
              'AlgoTrading.Portfolio',
              'AlgoTrading.Strategy',
              'AlgoTrading.examples',
              'AlgoTrading.Utilities',
              'AlgoTrading.tests'],
    py_modules=['AlgoTrading.__init__'],
    install_requires=io.open(requirements, encoding='utf8').read(),
    license='',
    author='cheng.li',
    author_email='wegamekinglc@hotmail.com',
    description='algorithmic trading framework for multiple assets'
)
