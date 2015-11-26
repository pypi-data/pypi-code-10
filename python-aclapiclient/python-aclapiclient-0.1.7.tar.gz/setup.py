#!/usr/bin/python
from setuptools import setup
from os.path import dirname, abspath, join
from pip.download import PipSession
from pip.req import parse_requirements


name = 'python-aclapiclient'

get_path = lambda *p: join(dirname(abspath(__file__)), *p)

install_reqs = parse_requirements(get_path('requirements.txt'), session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

VERSION = "0.1.7"

setup(
    name=name,
    version=VERSION,
    description="Python ACL API client",
    author='Time Storm',
    author_email='storm@corp.globo.com',
    url="http://ngit.globoi.com/python-aclapi/python-aclapi",
    packages=["aclapiclient"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)',
    ],
    install_requires=reqs,
)
