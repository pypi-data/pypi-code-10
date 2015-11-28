# -*- coding: utf-8 -*-
'''
python setup.py sdist upload
'''
from distutils.core import setup
from 試驗中介.版本 import 版本

_專案說明 = '''
提供前端開發時的功能試驗佮系統試驗的django後端中介軟體
'''


github網址 = 'https://github.com/sih4sing5hong5/django-tsi3giam7-tiong1kai3'

setup(
    name='django-tsi3giam7-tiong1kai3',
    packages=['試驗中介'],
    version=版本,
    description='提供前端開發時的功能試驗佮系統試驗的django後端中介軟體',
    long_description=_專案說明,
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='http://意傳.台灣/',
    download_url=github網址,
    keywords=[
        'function test',
        'system test',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
    ],
    install_requires=[
        'django',
    ],
)
