# coding: utf-8
from setuptools import setup, find_packages
 
setup (
    name = 'grunt4django',
    version = '1.0.1',
    py_modules = ['grunt4django'],
    author = 'lihao',
    author_email = 'lihao12518@163.com',
    description = '包含django的runserver命令，还有针对html的中间件(添加livereload)',
    packages = find_packages(),
)