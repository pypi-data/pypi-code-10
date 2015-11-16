#-*- coding:utf-8 -*-
'''
Author: whb
Date:2014-03-21
e-mail:hbnnlong@163.com
'''

import os
from mako.template import Template
from mako.lookup import TemplateLookup
from baseclass.send_email import SendMail

directory=os.path.join(os.environ.get('PackagePath'),'template/')

def data2html(data,tplname):
    
    lookup=TemplateLookup(directories=[directory],
                          input_encoding='utf8',
                          output_encoding='utf8',
                          encoding_errors='replace')
    tar=lookup.get_template(tplname)
    html=tar.render(data_list=data)
    return html
