from setuptools import setup

setup(name='ds_utils',
      version='0.4.1',
      description='Utilities for Hudl Data Science',
      long_description='Utilities used by the Data Science Squad at Hudl.'
                       'Includes a wrapper for Amazon Kinesis that provides easy logging.',
      author='Hudl R&D',
      url='http://hudl.github.io/',
      author_email='',
      maintainer='Nathan DeMaria',
      maintainer_email='nathan.demaria@hudl.com',
      license='MIT',
      install_requires=[
          'boto'
      ],
      packages=['ds_logger'],
      entry_points={}
      )
