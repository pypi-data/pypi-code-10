from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='niceconf',
    version='0.1.2',
    description='A nice config package',
    long_description=long_description,
    url='https://github.com/tdb-alcorn/niceconf',
    download_url='https://github.com/tdb-alcorn/niceconf/tarball/0.1.2',
    author='Thomas Alcorn',
    author_email='tdb.alcorn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Topic :: System',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='config configuration',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
