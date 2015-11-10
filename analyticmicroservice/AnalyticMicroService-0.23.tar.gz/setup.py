from distutils.core import setup
from setuptools import find_packages
import os
# http://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
if os.environ.get('USER','') == 'vagrant':
    del os.link

# from http://peterdowns.com/posts/first-time-with-pypi.html
# http://www.siafoo.net/article/77
# do 'python setup.py sdist upload -r pypi' to upload
# assumes ~/.pypirc file
setup(
    name='AnalyticMicroService',
    packages = find_packages(),
    version='0.23',
    description='Analytic Micro Service',
    author='datakitchen',
    author_email='cbergh@datakitchen.io',
    url='https://github.com/DataKitchen/AnalyticMicroService',
    download_url='https://github.com/DataKitchen/AnalyticMicroService/tarball/0.21',  # I'll explain this in a second
    keywords=['Analytic', 'microservice', 'service'],  # arbitrary keywords
    classifiers=[]
)
