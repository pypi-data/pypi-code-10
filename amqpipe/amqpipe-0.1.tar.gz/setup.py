#!/usr/bin/env python

from distutils.core import setup

setup(
    name='amqpipe',
    version='0.1',
    description='Twisted based pipeline framework for AMQP',
    license='GPL',
    author='Alexander Tikhonov',
    author_email='random.gauss@gmail.com',
    url='https://github.com/Fatal1ty/amqpipe',
    packages=['amqpipe'],
    install_requires=[
        'twisted',
        'pika',
        'colorlog']
)
