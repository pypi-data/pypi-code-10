#!/usr/bin/env python
#coding: utf8

import sys
import os
from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py
files = ["spouk_bottle_csrf/*", "spouk_bottle_csrf/example/*"]

setup(
    name = 'spouk-bottle-csrf',
    version = '0.0.1',
    url = 'http://spouk.ru',
    description = 'csrf  plugin for bottle',
    long_description = """csrf support for bottle
        server.py
        ---------
             #!/usr/bin/env python
             #coding: utf-8
             __author__ = 'spouk'

             from bottle import Bottle, template, TEMPLATE_PATH
             from  spouk_bottle_csrf import CSRF

             CSRF_SALT = 'somesalforcsrf'
             csrf = CSRF(CSRF_SALT=CSRF_SALT)

             app=Bottle()
             TEMPLATE_PATH.append('template/')
             app.install(csrf)


             # пример декоратора
             @app.csrf.csrf_decorator
             def mainrender(page, *argc,**kwargs):
                 kwargs.update(dict(app=app))
                 result = template(page, *argc, **kwargs)
                 # app.csrf.csrf_check_after_request(result)
                 return template(page, *argc, **kwargs)

             @app.get('/')
             def root():
                 print app.csrf.csrf_token, app.csrf.csrf_meta_geting
                 return mainrender('index.html')

             app.run(host='localhost',port=3500, debug=True,reloader=True)



        index.html
        ----------
            <html>
              <head>
                <meta charset="utf-8" />
                <meta content="{{app.csrf.csrf_token}}" name="csrf-token">
              </head>
            <body>

              Csrf_token: {{ app.csrf.csrf_token }} <br />
              example visible `hidden` input form:  {{ app.csrf.csrf_token_html }} <br />
              example `hidden` form:  {{ !app.csrf.csrf_token_html }}  <br />
            </body>
            </html>


        ---
        Copyleft [x] 2015, Spouk
    """,
    author = 'Spouk',
    author_email = 'spouk@spouk.ru',
    license = 'MIT',
    platforms = 'any',
    packages=['spouk_bottle_csrf'],
    package_data = {'spouk_bottle_csrf': files, 'spouk_bottle_csrf/example':files},
#    py_modules = [
#        'spouk_bottle_csrf',        
#    ],
    requires = [
        'bottle (>=0.9)',
        'bs4 (>=4.0.1)',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass = {'build_py': build_py}
)
