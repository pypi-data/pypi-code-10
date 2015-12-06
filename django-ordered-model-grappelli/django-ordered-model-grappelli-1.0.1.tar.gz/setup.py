#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
 
setup(
    name='django-ordered-model-grappelli',
    version='1.0.1',
    description='Allows Django models to be ordered and provides a simple admin interface for reordering them.',
    author='Grigoriy Bezyuk',
    author_email='me@gbezyuk.ru',
    url='http://github.com/gbezyuk/django-ordered-model-grappelli',
    packages=[
        'ordered_model',
        'ordered_model.tests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    package_data={'ordered_model': ['static/ordered_model/arrow-up.gif',
                                    'static/ordered_model/arrow-down.gif',
                                    'locale/de/LC_MESSAGES/django.po',
                                    'locale/de/LC_MESSAGES/django.mo',
                                    'locale/pl/LC_MESSAGES/django.po',
                                    'locale/pl/LC_MESSAGES/django.mo',
                                    'templates/ordered_model/admin/order_controls.html']}
)
