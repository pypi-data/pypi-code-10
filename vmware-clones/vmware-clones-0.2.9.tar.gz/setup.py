__author__ = 'gabriel'

from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

REQUIREMENTS = [
    "argparse==1.2.1",
    "pyvmomi==5.5.0.2014.1.1",
    "requests==2.7.0",
    "six==1.9.0",
    "wsgiref==0.1.2",
    "Jinja2==2.8",
]

PLATFORMS = [
    'OS Independent'
]

PACKAGES = [
    'vclones',
]

DATA = [
    (
        '/opt/vclones', [
            'requirements.txt',
            'email_notification.html',
            'esxi.ini.sample'
        ]
    )
]

ENTRY_POINTS = {
    'console_scripts': [
        'vmwareclone-batch = vclones:batch',
        'vmwareclone = vclones:main',
        'vmwareclone-test = vclones:test'
    ]
}

setup(
    name='vmware-clones',
    version='0.2.9',
    author="Gabriel Melillo",
    author_email="gabriel@melillo.me",
    maintainer="Gabriel Melillo",
    maintainer_email="gabriel@melillo.me",
    description="Clone running vmware virtual machines running on preconfigured cluster",
    url="https://github.com/gmelillo/esxi-backup",
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    platforms=PLATFORMS,
    data_files=DATA,
    include_package_data=True,
    packages=PACKAGES,
    license="GNU GENERAL PUBLIC LICENSE",
    long_description='Clone all running virtual machines in a running vmware cluster to a specified VCSA'
                     '\n\n',
    entry_points=ENTRY_POINTS
)


