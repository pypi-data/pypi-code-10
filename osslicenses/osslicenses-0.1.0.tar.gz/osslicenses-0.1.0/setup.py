from setuptools import setup

setup(
    name='osslicenses',
    version='0.1.0',
    description='CLI for viewing OSS licenses',
    author='Matt Chung',
    author_email='Matt Chung',
    url='https://github.com/itsmemattchung/osslicenses',
    download_url='https://github.com/itsmemattchung/osslicenses/tarball/0.1',
    keywords=[
        'oss',
        'licenses'
    ],
    install_requires=[
        'click',
        'tabulate'
    ],
    dependency_links=[
        'git+ssh://git@github.com/sigmavirus24/github3.py@develop'
    ],
    entry_points='''
        [console_scripts]
        osslicenses=osslicenses.cli:cli
    '''
)
