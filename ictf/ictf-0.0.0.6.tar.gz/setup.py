from distutils.core import setup

setup(
    name='ictf',
    version='0.0.0.6',
    description='This is a python module that provides an interface to the iCTF team API.',
    packages=['ictf'],
    install_requires=[
        'requests',
    ],
)
