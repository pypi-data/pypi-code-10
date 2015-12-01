# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='wagtail-stacks-image',
    packages=find_packages(),
    version='0.1',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://stacks.wgbhdigital.org/',
    license='MIT License, see LICENSE',
    description=(
        "A Wagtail Stacks application for handling images and lists of images."
    ),
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=['wagtail-streamfieldtools>=0.1'],
    include_package_data=True,
    package_data={
        'wagtail_stacks_image': [
            'static/sass/*.scss',
            'static/js/*.js',
            'static/js/vendor/lazyimages/*.js',
            'static/js/vendor/owl/*.js',
            'templates/wagtail_stacks_image/single/*.html',
            'templates/wagtail_stacks_image/list/*.html'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
