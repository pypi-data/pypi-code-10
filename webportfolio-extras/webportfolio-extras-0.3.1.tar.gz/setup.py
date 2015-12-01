"""
Webportfolio extras
"""

from setuptools import setup, find_packages

__version__ = "0.3.1"
setup(
    name="webportfolio-extras",
    version=__version__,
    license="MIT",
    author="Mardix",
    author_email='mardix@pylot.io',
    description="WebPortfolio extra packages",
    long_description=__doc__,
    url='http://github.com/mardix/webportfolio-extras/',
    download_url='http://github.com/mardix/webportfolio-extras/tarball/master',
    py_modules=['webportfolio_extras'],
    keywords=["webportfolio", "rq", "queue", "redis"],
    include_package_data=True,
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'boto',
        'rq==0.5.3',
        'redis==2.9.1',
        "redis-collections==0.1.7",
        "rollbar",
        "newrelic",
        "mutagen==1.31"
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
