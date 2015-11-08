from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='make_excel',

    version='1.2.0.dev1',

    description='Create .xls file with Python dictionary',
    long_description=long_description,

    url='https://github.com/nidhinbose89/make_excel.git',

    author='Nidhin Bose J',
    author_email='nidhinb@yahoo.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',

    ],

    keywords='Create .xls file with Python dictionary',

    py_modules=["make_excel"],

    install_requires=['xlwt', 'xlrd', 'xlutils'],

    entry_points={
        'console_scripts': [
            'make_excel=make_excel:make_excel',
        ],
    },
)
