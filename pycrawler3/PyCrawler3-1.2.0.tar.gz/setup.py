from setuptools import setup
setup(
  name='PyCrawler3',
  packages=['pycrawler'],  # must be filled with your python directories
  version='1.2.0',
  description='A Python crawler tool to grab page(s) information from html data. This only support Python 3',
  author='Aditya Kresna Permana',
  author_email='zeandcode@gmail.com',
  url='https://github.com/slaveofcode/pycrawler',
  download_url='https://github.com/slaveofcode/pycrawler/archive/v1.2.0.zip',
  install_requires=[
      'JPype1==0.6.1',
      'JPype1-py3==0.5.5.2',
      'beautifulsoup4==4.4.1',
      'boilerpipe-py3==1.2.0.0',
      'charade==1.0.3',
      'requests==2.8.1'
  ],
  keywords=[
      'crawler',
      'pycrawler',
      'boilerpipe',
      'boilerpipe3',
      'page crawler',
      'html crawler',
      'document crawler'
  ],
  classifiers=[],
)