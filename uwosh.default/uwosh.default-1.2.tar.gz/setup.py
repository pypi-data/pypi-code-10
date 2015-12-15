from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='uwosh.default',
      version=version,
      description="default settings for uwosh plone sites",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://github.com/uwosh/uwosh.default',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uwosh'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'uwosh.core>=0.3.4b1',
        'plone.browserlayer'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
