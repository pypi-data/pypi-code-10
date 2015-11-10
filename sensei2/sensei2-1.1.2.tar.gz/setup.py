import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'readme.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sensei2',
    version='1.1.2',
    packages=['sensei2'],
    url='https://bitbucket.org/dvebukvy/sensei2/',
    include_package_data=True,
    license='DB',
    author='kirill',
    author_email='kirillkostuykhin@me.com',
    description='A tool to fill your database with random, but logical data',
    long_description=README,
    install_requires=['Pillow', 'pytils', 'django-autoslug','termcolor']
)
