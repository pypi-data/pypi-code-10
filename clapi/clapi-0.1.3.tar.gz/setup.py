try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='clapi',
    packages=['clapi'],
    version='0.1.3',
    description='CLAPI wrapper',
    install_requires=[],
    author='Robert Wikman',
    author_email='rbw@vault13.org',
    maintainer='Robert Wikman',
    maintainer_email='rbw@vault13.org',
    url='https://github.com/rbw0/python-clapi',
    download_url='https://github.com/rbw0/python-clapi/tarball/0.1.3',
    keywords=['clapi', 'wrapper', 'Centreon'],
    classifiers=[],
    license='GPLv2',
)
