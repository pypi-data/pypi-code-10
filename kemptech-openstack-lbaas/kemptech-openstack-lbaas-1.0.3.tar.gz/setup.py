#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup
from setuptools import find_packages

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name="kemptech-openstack-lbaas",
      version="1.0.3",
      packages=find_packages(),
      author="KEMP Technologies",
      author_email="smcgough@kemptechnologies.com",
      maintainer="Shane McGough",
      maintainer_email="smcgough@kemptechnologies.com",
      description="KEMP Technologies OpenStack LBaaS Driver V2",
      long_description=open('README.rst').read(),
      license="Apache",
      keywords="kemptech kemp technologies lbaas load balancer driver",
      url="http://pypi.python.org/pypi/kemptech-openstack-lbaas/",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Internet',
      ],
      install_requires=reqs
)
