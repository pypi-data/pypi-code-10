#encoding:utf-8
from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(
    name = 'SendRequest',
    version = '0.2',
    description = 'http request with retry, text decode, unzip and so on.封装网络请求，自带重试，返回文本转码，解压缩等',
    packages = find_packages()
)
