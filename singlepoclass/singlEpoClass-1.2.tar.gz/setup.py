from setuptools import setup, find_packages
import os

setup(name='singlEpoClass',
      version='1.2',
      description='Single Epoch Transient Classifier',
      url='http://github.com/sofiatti/SingleEpochPhotometricClassifier',
      author='Caroline Sofiatti',
      author_email='sofiatti@berkeley.edu',
      packages=find_packages(),
      scripts=['scripts/' + f for f in os.listdir('scripts')],
      zip_safe=False)
