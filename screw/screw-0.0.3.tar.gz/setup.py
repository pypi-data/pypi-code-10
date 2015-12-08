#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages

setup(name="screw",
      version="0.0.3",
      keywords=('screw', 'egg'),
      description='screw egg',
      license='MIT License',

      url="http://yinwentao.com/",
      author="yoon",
      author_email="yinwentao312@gmail.com",

      packages=find_packages(),
      include_package_data=True,
      platforms='any',
      install_requires=[],
      entry_points={'console_scripts': ['screw=screw.shell:main']}
      )

