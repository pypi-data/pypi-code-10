#!/usr/bin/env python
#coding: utf-8
__author__ = 'spouk'

import bottle
import random
import bs4
import functools
import hashlib
import uuid

__all__ = ['CSRF']

class CSRF(object):
    name = "CSRF"
    api = 2
    __doc__ = """CSRF класс, использует bottle.request для отслеживания
    типа запроса если `POST` генерирует ДО вызова новый токен, дампит его в
    локальном 2-элемнтном стеке
    self.csrf_token_html - свойство, рендерит html представление с текущим значением токена
    self.csrf_decorator - декоратор для функции рендеринга, пример привел в описании декоратора
    self.csrf_check_after_request - проверяет входящие значение токенов <meta..> при всех запросах, и формы - при POST запросах
    и сохраняет в соответствующих аттрибутах .csrf_meta_getting, .csrf_post_getting
    """
    def __init__(self, CSRF_SALT = None):

        # полученые токены от пользователя
        self.csrf_meta_geting = None
        self.csrf_post_geting = None

        # оригинальные токены
        self.csrf_stack = []
        self.csrf_token = None

        # общие атрибуты/функции
        self.csrf_salt  = CSRF_SALT
        self.request = bottle.request
        self.csrf_session_salt = self.csrf_salt or random.gammavariate(10,200)
        self.app = None

    @property
    def csrf_token_html(self):
        return '<input type="hidden" name="csrf-token" value="{token}" />"'.format(token=self.csrf_token)

    def setup(self, app):
        __doc__  = "setup for bottle"
        self.app = app
        self.app.csrf = self
        self.app.add_hook("before_request", self.csrf_generate)

    def apply(self, callback, context):
        __doc__  = "apply for bottle plugin"
        return callback

    def csrf_generate(self):
        __doc__ = "создает новый уникальный csrf_token"
        print '[CSRF] call generate new token'
        if self.csrf_token is None:
            self.csrf_token = hashlib.md5(str(uuid.uuid4())+str(self.csrf_session_salt)).hexdigest()
            self.csrf_stack.append(self.csrf_token)

        if self.csrf_token and not self.csrf_stack:
            self.csrf_stack.append(self.csrf_token)

        if self.request.method == "POST":
            self.csrf_token = hashlib.md5(str(uuid.uuid4())+str(self.csrf_session_salt)).hexdigest()
            if len(self.csrf_stack) == 2:
                self.csrf_stack.pop(0)
            self.csrf_stack.append(self.csrf_token)

    def csrf_check_after_request(self, page=None, parser=None):
        """проверка значения csrf токена после получения POST, получает из поля
        input с именем `csrf_token` значение и сохраняет его в `self.gettoken`
        если такого поля нет, пробует получить `META` значение токена с названием
        `csrf_token`, можно для скорости сменить парсер на  lxml
        """
        # получаю META токен при всех запросах
        if page:
            pars_result = bs4.BeautifulSoup(page, parser or "html.parser").findAll('meta')
            found = filter(lambda x: x.get('name',None) and x.get('name') == 'csrf-token', pars_result)
            self.csrf_meta_geting = found and found[0].get('content', None) or None

        # обработка после POST запроса, и попытка получение токена из отправленной формы
        if self.request.method == "POST":
            self.csrf_post_geting  = self.request.forms.get('csrf-token')

    def csrf_decorator(self, f):
        __doc__  = """ декоратор для функции рендеринга
        пример:
        server.py
        ---------
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
            <meta content='{{app.csrf.csrf_token}}' name='csrf-token' />
        </head>
        <body>
             {{ app.csrf.csrf_token }}
             {{ !app.csrf_token_html }} -> html рендеринг скрытой формы
        </body>

        """
        @functools.wraps(f)
        def decor(*argc, **kwargs):
            result = None
            try:
                result = f(*argc, **kwargs)
                self.csrf_check_after_request(result)
            except Exception as error:
                pass
            return result
        return decor
