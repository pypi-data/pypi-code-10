# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.9.20',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'更新http模块，修改is_wechat模块，判断是否是微信浏览器',
    package_data = {
        '': ['*.data'],
    },
)