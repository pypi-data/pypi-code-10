# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='wagtail-stacks',
    packages=find_packages(),
    version='0.1',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://stacks.wgbhdigital.org/',
    license='MIT License, see LICENSE',
    description=(
        "A Wagtail Stacks app for creating links."
    ),
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=['wagtail>=1.2'],
    package_data={
        'wagtail_stacks': [
            'templates/wagtail_stacks/*.html',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'
    ]
)
