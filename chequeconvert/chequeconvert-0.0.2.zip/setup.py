import sys
from setuptools import find_packages
from setuptools import setup
import io
import os

VERSION = '0.0.2'


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(fpath(filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def get_requirements():
    requires = [line.rstrip('\n') for line in open(fpath('requirements.txt'))]

    if sys.version_info[:2] == (2, 6):
        # For python2.6 we have to require argparse since it was not in stdlib until 2.7.
        requires.append('argparse')
    return requires


setup_args = dict(
    name='chequeconvert',
    description='Convert amount to word for cheque writing',
    url='https://github.com/pirsquare/chequeconvert-python',
    version=VERSION,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'chequeconvert = chequeconvert.main:main',
        ],
    },
    include_package_data=True,
    install_requires=get_requirements(),
    author='Ryan Liao',
    author_email='pirsquare.ryan@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
