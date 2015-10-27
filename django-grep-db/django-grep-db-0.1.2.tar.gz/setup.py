import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-grep-db',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,

    description='A simple Django app for command-line searching via the ORM',
    long_description=README,
    keywords='django search grep cli',
    license='MIT',
    author='Michael Blatherwick',
    author_email='michael.blatherwick@exeter.oxon.org',
    url='https://github.com/exonian/django-grep-db',
)
