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
    version = '0.0.2',
    url = 'http://spouk.ru',
    description = 'csrf  plugin for bottle',
    long_description = """csrf support for bottle
        server.py
        ---------
             #!/usr/bin/env python
             #coding: utf-8
             __author__ = 'spouk'

             #---------------------------------------------------------------------------
             #   global imports
             #---------------------------------------------------------------------------

             from bottle import Bottle, TEMPLATE_PATH, request
             from  jinja2 import  Environment, FileSystemLoader
             from  spouk_bottle_csrf import CSRF

             #---------------------------------------------------------------------------
             #   set variables.../app/other stuff
             #---------------------------------------------------------------------------

             CSRF_SALT = 'somesalforcsrf'
             TEMPLATE_PATH.append('template/')
             env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
             csrf = CSRF(csrf_salt=CSRF_SALT)

             app=Bottle()
             app.install(csrf)


             #---------------------------------------------------------------------------
             #   definintion render, inject some map links variables
             #---------------------------------------------------------------------------

             def jinja(page, *args, **kwargs):

                 kwargs.update(dict(url_for=app.get_url))
                 kwargs.update(dict(csrf_html=app.csrf.csrf_html))
                 kwargs.update(dict(request=request))
                 kwargs.update(dict(app=app))
                 tpl = env.get_template(page)
                 return tpl.render(*args, **kwargs)

             #---------------------------------------------------------------------------
             #   routing map
             #---------------------------------------------------------------------------

             @app.get('/')
             def root():
                 return jinja('index.html')

             @app.post('/', name="root")
             def root_post():
                 # check validate tokens
                 print request.forms.get('csrf_token', None) == app.csrf.csrf_token_last and "Form and csrf token validate" or "Invalid csrf token"
                 return  jinja('index.html')

             app.run(host='localhost',port=3500, debug=True,reloader=True)


        index.html
        ----------
             <html>
               <head>
                 <meta charset="utf-8" />
                 <meta content="{{app.csrf.csrf_token}}" name="csrf_token">
               </head>
             <body>
             <h3> User form </h3>
             <hr/>
                  <form  method="post" action="{{ url_for('root')}}">
                         {{ csrf_html() }}
                     Username: <input type="text" name="username" >
                     Password: <input type="password" name="password">
                     <input type="submit" name="sender" value="Login">
                  </form>
             <hr/>
             {% if request.method == "POST" %}
                <h3> Result validate form </h3>
                <br/>
                <p> Validate result: {{app.csrf.csrf_last ==  request.form.get('csrf_token',None)}}

             {% endif %}

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
#    package_data = {'spouk_bottle_csrf':},
    py_modules = [
            'spouk_bottle_csrf',
    ],
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
