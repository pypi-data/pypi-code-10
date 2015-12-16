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
    """ render page  """

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
    result = request.forms.get('csrf_token', None) == app.csrf.csrf_token_last and "Form and csrf token validate" or "Invalid csrf token"
    return  jinja('index.html', result=result)

app.run(host='localhost',port=3500, debug=True,reloader=True)
