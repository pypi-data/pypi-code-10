import os

from setuptools import setup

import postmark_inbound as app

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = open('requirements.txt').read().splitlines()

setup(
    name='django-postmark-inbound',
    version=app.__version__,
    packages=['postmark_inbound'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Simple API webhook to accept inbound mail requests processed by Postmark (www.postmarkapp.com).',
    long_description=README,
    url='https://github.com/christippett/django-postmark-inbound',
    author='Chris Tippett',
    author_email='c.tippett@gmail.com',
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email'
    ],
)
