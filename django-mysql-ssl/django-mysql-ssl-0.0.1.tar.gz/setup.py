import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='django-mysql-ssl',
    version='0.0.1',
    author='CFPB',
    author_email='tech@cfpb.gov',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/cfpb/django-mysql-ssl',
    license='Public Domain',
    description=u'Backport dbshell support for ssl mysql connections in Django < 1.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=read_file('README.md'),
    zip_safe=True,
)
