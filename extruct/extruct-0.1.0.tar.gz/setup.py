# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


def get_version():
    path = os.path.join(
        os.path.dirname(__file__), 'extruct', 'VERSION')
    with open(path) as f:
        return f.read().strip()


requirements = []

setup(
    name='extruct',
    version=get_version(),
    description='Extract embedded metadata from HTML markup',
    author='Scrapinghub',
    author_email='info@scrapinghub.com',
    maintainer='Scrapinghub',
    maintainer_email='info@scrapinghub.com',
    url='https://github.com/scrapinghub/extruct',
    packages=find_packages(include=['extruct']),
    package_data={'extruct': ['VERSION']},
    install_requires=['lxml'],
    extras_require={
        'service': [
            'bottle',
            'gevent',
        ]
    },
    keywords='extruct',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
