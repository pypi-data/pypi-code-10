"""
Webportfolio extras
"""

from setuptools import setup

__version__ = "0.1.0"
setup(
    name="webportfolio-extras",
    version=__version__,
    license="MIT",
    author="Mardix",
    author_email='mardix@pylot.io',
    description="RQ Worker wrapper for WebPortfolio",
    long_description=__doc__,
    url='http://github.com/mardix/webportfolio-extras/',
    download_url='http://github.com/mardix/webportfolio-extras/tarball/master',
    py_modules=['webportfolio_extras'],
    keywords=["webportfolio", "rq", "queue"],
    platforms='any',
    install_requires=[
        "webportfolio_rq_worker",
        "redis-collections==0.1.7",
        "rollbar",
        "newrelic"
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
