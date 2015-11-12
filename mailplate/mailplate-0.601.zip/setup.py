from setuptools import setup

setup(
    name = 'mailplate',
    packages = [ 'mailplate' ],
    package_data = { 'mailplate': [ 'driver/*.py' ]},
    version = '0.601',
    description = 'Send Muli-Language Multi-Transport Template-Driven Email',
    author = 'Avner Herskovits',
    author_email = 'avnr_ at outlook.com',
    url = 'https://github.com/avnr/mailplate',
    download_url = 'https://github.com/avnr/mailplate/tarball/0.601',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
    ],
)
