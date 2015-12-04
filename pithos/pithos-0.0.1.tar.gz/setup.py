#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='pithos',
    version='0.0.1',
    description='Session handling for web application',
    author='Rudolph Froger',
    author_email='rudolphfroger@dreamsolution.nl',
    maintainer='Rudolph Froger',
    maintainer_email='rudolphfroger@dreamsolution.nl',
    url='https://github.com/Dreamsolution/pithos',
    license='MIT',
    packages=['pithos'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "six>=1.10,<2",
        "cryptography>=1.1,<1.2",
        "simplejson>=3.8,<4.0",
    ],
    extras_require = {
        'redis': ['redis>=2.10,<3'],
    },
    tests_require=['pytest', 'flake8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        # FIXME Test with Python 2.7
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
