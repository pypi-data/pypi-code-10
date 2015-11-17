#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-sqs-qc',
    version="0.2",
    description='django package to use existing Amazon SQS Queue',
    author='Nauman Tariq',
    author_email='nauman3128@gmail.com',
    url='https://github.com/nauman3128/sqs-django-qc',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)

