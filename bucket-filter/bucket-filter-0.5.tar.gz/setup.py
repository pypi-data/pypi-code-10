from distutils.core import setup
import os

def read(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()

setup(
        name='bucket-filter',
        version='0.5',
        packages=['bucket_filter'],
        url='https://github.com/conlini/bucket_filters',
        license='Apache License, Version 2.0',
        author='adityabhasin',
        author_email='conlini@gmail.com',
        description='A filtering library to present data that matches a series of conditional expressions',
        long_description=read("README.rst")
)
