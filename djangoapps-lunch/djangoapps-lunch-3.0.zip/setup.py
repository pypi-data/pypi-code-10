#coding:UTF-8
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangoapps-lunch',
    version='3.0',
    packages=['bases','lunchapp','usercenter'],
    include_package_data=True,
    license='BSD License',  # example license
    description='lunchapp only chinese support',
    long_description=README,
    install_requires=['django==1.8','djangorestframework==3.1.3','markdown==2.6.2','django-filter==0.10.0','django-rest-auth==0.4.0','django-allauth==0.23.0'],
    url='no',
    author='XUE QING',
    author_email='xueqingwell@hotmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
