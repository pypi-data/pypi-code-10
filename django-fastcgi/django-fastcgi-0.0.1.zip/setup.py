from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-fastcgi',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['Django'],
    description='Exposes a management command to connect to FastCGI server'
)
