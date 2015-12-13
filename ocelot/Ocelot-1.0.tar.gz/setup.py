#!/usr/bin/env python

from distutils.core import setup


setup(
    name='Ocelot',
    version='1.0',
    description='Static site generator designed for stories',
    author='Damien Howard',
    author_email='foxscotch@gmail.com',
    url='http://foxscotch.us/',
    py_modules=['ocelot'],
    requires=[
        'Markdown',
        'Jinja2',
        'PyYaml'
    ]
)
