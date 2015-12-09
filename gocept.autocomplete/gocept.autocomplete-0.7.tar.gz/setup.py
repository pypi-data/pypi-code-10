import os.path
from setuptools import setup, find_packages


def read(*path):
    """Read a file from the path."""
    return open(os.path.join(*path)).read()

setup(
    name='gocept.autocomplete',
    version='0.7',
    author='gocept',
    author_email='mail@gocept.com',
    description='AJAX autocomplete widget for z3c.form',
    long_description='\n\n'.join([
        read('COPYRIGHT.txt'),
        read('src', 'gocept', 'autocomplete', 'README.txt'),
        read('HACKING.txt'),
        read('CHANGES.txt'),
    ]),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://bitbucket.org/gocept/gocept.autocomplete',
    zip_safe=False,
    license='ZPL 2.1',
    namespace_packages=['gocept'],
    classifiers="""\
Development Status :: 4 - Beta
Framework :: Zope3
Intended Audience :: Developers
License :: OSI Approved
License :: OSI Approved :: Zope Public License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 2 :: Only
Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: Libraries
"""[:-1].split('\n'),
    install_requires=[
        'js.jqueryui',
        'setuptools',
        'z3c.form',
        'zope.browser',
        'zope.component',
        'zope.interface',
        'zope.pagetemplate',
        'zope.publisher',
        'zope.schema',
        'zope.traversing',
    ],
    extras_require=dict(
        test=[
            'lxml',
            'gocept.selenium',
            'zope.app.appsetup',
            'zope.app.testing',
            'zope.app.zcmlfiles',
            'zope.securitypolicy',
            'zope.server',
            'zope.app.server',
            'zope.testing',
            'zope.testbrowser>=3.4.3',
        ]),
)
