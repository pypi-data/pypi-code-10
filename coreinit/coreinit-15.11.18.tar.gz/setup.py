#from distutils.core import setup
from setuptools import setup,find_packages

setup(
  name = 'coreinit',
  packages = find_packages(),
  version = '15.11.18',
  description = 'Service autodeploy and autoconfig library',
  author = 'Marta Nabozny',
  author_email = 'martastrzet@gmail.com',
  url = 'http://cloudover.org/coreinit/',
  download_url = 'https://github.com/cloudOver/CoreInit/archive/master.zip',
  keywords = ['overcluster', 'cloudover', 'cloud'],
  include_package_data = True,
  package_data = {
    'coreinit': ['templates/*.conf', 'templates/*.txt'],
  },
  classifiers = [],
  install_requires = []
)
