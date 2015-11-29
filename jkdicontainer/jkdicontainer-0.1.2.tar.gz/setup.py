from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='jkdicontainer',
    version='v0.1.2',
    description='',
    long_description=long_description,
    author='Jakub Kanclera',
    author_email='jakub.kanclerz@gmail.com',
    url='',
    py_modules=['container'],
    license='MIT',
    keywords=[],
    test_suite='tests'
)