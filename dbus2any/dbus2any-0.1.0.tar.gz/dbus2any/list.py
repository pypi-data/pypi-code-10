# -*- coding: utf-8 -*-

from os import path, listdir


def templates_list():
    cur = path.dirname(__file__)
    return listdir(path.join(cur, 'templates'))


def list_templates():
    templates = templates_list()
    for template in templates:
        print(template)


def read_template(template):
    if template.startswith(path.sep) or \
            template.startswith('~'):
        with open(path.abspath(template)) as tpl:
            return  tpl.read()

    for tpl_name in templates_list():
        if tpl_name == template:
            cur = path.abspath(path.dirname(__file__))
            with open(path.join(cur, 'templates', template)) as tpl:
                return  tpl.read()
    raise FileNotFoundError()
