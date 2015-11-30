# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='eureka-client',
    version='0.6.2',
    description='A python interface for Netflix Eureka',
    author=u'Jorge Dias',
    author_email='jorge@mrdias.com',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=[]),
    install_requires=[
        'dnspython'
    ],
)
