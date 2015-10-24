from distutils.core import setup
import setuptools
setup(
  name = 'mongo_cache',
  packages = ['mongo_cache'], # this must be the same as the name above
  version = '0.1.1',
  description = 'A library for a cache backed by mongodb',
  author = 'Karthik T',
  author_email = 'karthikt.holmes+github@gmail.com',
  url = 'https://github.com/ktaragorn/mongo_cache', # use the URL to the github repo
  download_url = 'https://github.com/ktaragorn/mongo_cache/tarball/0.1.1',
  keywords = ['cache', 'mongodb'], # arbitrary keywords
  install_requires=[
    'pymongo',
  ],
  classifiers = [],
)