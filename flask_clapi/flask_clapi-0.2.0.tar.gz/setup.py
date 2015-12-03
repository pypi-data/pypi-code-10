try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='flask_clapi',
    packages=['flask_clapi'],
    version='0.2.0',
    description='CLAPI wrapper',
    install_requires=['clapi'],
    author='Robert Wikman',
    author_email='rbw@vault13.org',
    maintainer='Robert Wikman',
    maintainer_email='rbw@vault13.org',
    url='https://github.com/rbw0/flask_clapi',
    download_url='https://github.com/rbw0/flask_clapi/tarball/0.2.0',
    keywords=['flask', 'clapi', 'wrapper', 'Centreon'],
    classifiers=[],
    license='GPLv2',
)
