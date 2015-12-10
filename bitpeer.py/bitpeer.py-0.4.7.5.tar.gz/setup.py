from setuptools import setup
import bitpeer


setup(
    name='bitpeer.py',
    version='0.4.7.5',
    url='https://github.com/dakk/bitpeer.py',
    license='BSD License',
    author='Davide Gessa, Christian S. Perone',
    author_email='gessadavide@gmail.com, christian.perone@gmail.com',
    description='A pure Python3 bitcoin protocol implementation.',
    long_description='A pure Python3 bitcoin protocol implementation.',
    install_requires=['ecdsa>=0.10', 'pycoin==0.62'],
    packages=['bitpeer', 'bitpeer.storage'],
    keywords='bitcoin, protocol, blockchain, litecoin, testnet, bitpeer, peer',
    platforms='Any',
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
