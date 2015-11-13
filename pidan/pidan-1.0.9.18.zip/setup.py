# install:python setup.py sdist upload

from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.9.18',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = 'modify http,add http.is_wechat method',
    package_data = {
        '': ['*.data'],
    },
)