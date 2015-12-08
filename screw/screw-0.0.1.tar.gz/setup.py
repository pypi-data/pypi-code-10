#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages

setup(name="screw",
      version="0.0.1",
      keywords=('screw', 'bee'),
      description='screw egg',
      license='MIT License',

      url="http://sac-blog.sac.sogou/",
      author="ywt",
      author_email="yinwentao@sogou-inc.com",

      packages = find_packages(),
      include_package_data = True,
      platforms = 'any',
      install_requires = [],)

