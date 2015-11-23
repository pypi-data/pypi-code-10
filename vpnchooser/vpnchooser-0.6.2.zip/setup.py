# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

requires = [
    'Flask==0.10.1',
    'Flask-RESTful==0.3.2',
    'Flask-Script==2.0.5',
    'Flask-SQLAlchemy==2.0',
    'paramiko',
    'passlib',
    'celery',
    'redis',
]

setup(
    name='vpnchooser',
    version='0.6.2',
    description='Web UI to switch clients between different ip rule tables',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Framework :: Flask",
        "Topic :: System :: Networking",
    ],
    author='Christoph Brand',
    author_email='christoph@brand.rest',
    keywords=['vpn', 'network', 'ip'],
    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},  # tell distutils packages are under src
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    url='https://github.com/cbrand/vpnchooser',
    download_url='https://github.com/cbrand/vpnchooser/tarball/0.6.1',
    entry_points={
        'console_scripts': [
            'vpnchooser=vpnchooser.manage:main'
        ]
    },
)
