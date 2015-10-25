try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ethjsonrpc',
    version='0.2.4',
    description='Ethereum JSON-RPC client',
    long_description=open('README.rst').read(),
    author='ConsenSys',
    author_email=['info@consensys.net'],
    url='https://github.com/ConsenSys/ethjsonrpc',
    packages=['ethjsonrpc'],
    license='Unlicense',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    install_requires=[
        'ethereum==1.0.6',
        'requests==2.8.1',
    ],
)
