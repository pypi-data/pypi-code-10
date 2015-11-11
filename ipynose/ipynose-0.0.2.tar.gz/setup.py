"""
Reference:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/ipynoseproject
https://pythonhosted.org/an_example_pypi_project/setuptools.html
"""

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ipynose',
    version='0.0.2',
    description='print nosetests result in the iPython notebook',
    long_description=read('README.rst'),
    url='https://github.com/wikibootup/ipynose',
    author='wikibootup',
    author_email='wikibootup@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='nose',
    install_requires=['nose'],
    packages=['ipynose'],
)

