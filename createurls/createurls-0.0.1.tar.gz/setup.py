from distutils.core import setup
from setuptools import find_packages

DESCRIPTION = 'Create urls suited for jmeter tests from apache logs'
print(find_packages())
setup(
    name='createurls',
    version='0.0.1',
    install_requires=[
        'tback-apachelog',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'createurls = createurls:main',
        ]
    },
    url='https://github.com/tback/createurls',
    license='MIT',
    author='Brandon Konkle',
    author_email='unknown@example.org',
    maintainer='Till Backhaus',
    maintainer_email='till@backha.us',
    description=DESCRIPTION,
    long_description=DESCRIPTION + '\n\nBased on https://lincolnloop.com/blog/2012/sep/19/load-testing-jmeter-part-3-replaying-apache-logs/',
)
