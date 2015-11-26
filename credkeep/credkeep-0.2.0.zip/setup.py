from credkeep import __version__
from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='credkeep',
    version=__version__,
    author='Jared Lewis',
    author_email='jared@jared.kiwi.nz',
    description='Store credentials securely as ciphertext and decrypt on the fly with AWS KMS',
    long_description=long_description,
    license='MIT',
    url='https://github.com/lewisjared/credkeep',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2'
    ],
    keywords='kms credentials storage encrypt decrypt',
    install_requires=['boto3>=1.1.1'],
    entry_points={
        'console_scripts':
            ['credkeep = credkeep.cli:main']
    },
    packages=find_packages(exclude='tests')
)
