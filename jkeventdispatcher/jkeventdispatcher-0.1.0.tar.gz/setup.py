from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='jkeventdispatcher',
    version='v0.1.0',
    description='',
    long_description=long_description,
    author='Jakub Kanclerz',
    author_email='jakub.kanclerz@gmail.com',
    url='',
    py_modules=['eventdispatcher'],
    license='MIT',
    keywords=[],
    test_suite='tests'
)