from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='maxleap-sdk',
    version='0.2.0',
    description='MaxLeap Python SDK',

    url='https://leap.as/',

    author='czhou',
    author_email='czhou@ilegendsoft.com',

    license='LGPL',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='MaxLeap SDK',

    packages=['ML'],

    package_dir={'ML':'ML'},

    package_data={'ML':['*.py']},

    test_suite='nose.collector',

    install_requires=[
        'requests>=2.4.3',
        'iso8601',
        'arrow',
        'flask',
    ],

    extras_require={
        'dev': ['sphinx'],
        'test': ['nose', 'coverage'],
    },
)
