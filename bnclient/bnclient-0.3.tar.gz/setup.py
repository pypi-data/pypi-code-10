# Copyright 2010 Blade Network Technologies

from distutils.core import setup

setup(name='bnclient',
      version='0.3',
      description="Blade Network Technologies Netconf Python Client",
      author="Jeff Sun",
      author_email="jeff.sun@bladenetwork.net",
      packages=["bnclient", "bnclient/rpc"],
      license="Blade Network Technologies",
      platforms=["Linux; Windows"],
      url = 'https://github.com/kderynski/blade-netconf-python-client',
      download_url = 'https://github.com/kderynski/blade-netconf-python-client/tarball/0.3',
      keywords = ['bnclient','netconf'],
      classifiers = [],
      )
