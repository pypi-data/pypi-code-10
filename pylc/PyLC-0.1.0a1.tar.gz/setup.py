from setuptools import setup, find_packages

setup(
  name='PyLC',
  version='0.1.0a1',
  author='Benjamin Morrise',
  author_email='bmorrise@gmail.com',
  description='A python wrapper for the Lending Club API',
  license='MIT',
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',    
  ],
  packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"])
)