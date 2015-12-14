#!/usr/bin/env python
#coding: utf-8
__author__ = 'spouk'

from bottle import Bottle, template, TEMPLATE_PATH
from  spouk_bottle_csrf import CSRF

CSRF_SALT = 'somesalforcsrf'
# вы можете не давать соли, по дефолту берет гаммазначение из `random`
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
