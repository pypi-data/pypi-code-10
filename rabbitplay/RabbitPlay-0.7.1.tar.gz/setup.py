"""
RabbitPlay
-------------

Abstraction on top of pika library for working with RabbitMQ.
"""
from setuptools import setup

setup(
    name="RabbitPlay",
    version="0.7.1",
    url='https://github.com/SwipeBank/rabbitplay',
    download_url='https://github.com/SwipeBank/rabbitplay/archive/0.7.1.tar.gz',
    author='Eugene <f0t0n> Naydenov, Michael <m1kev> Voropaiev',
    author_email='t.34.oxygen@gmail.com, m.voropaiev@gmail.com',
    description='Abstraction on top of pika for working with RabbitMQ.',
    long_description=__doc__,
    py_modules=['rabbitplay'],
    install_requires=[
        'pika==0.10.0'
    ],
)
