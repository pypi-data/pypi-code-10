from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
version='0.3.4'

setup(
    name='tornkts',
    version=version,
    description='Tuned Tornado classes for simpler creation of powerful APIs',
    long_description='Tuned Tornado classes for simpler creation of powerful APIs',

    author='KTS',
    author_email='tornkts@ktsstudio.ru',
    url='https://github.com/KTSStudio/tornkts',
    download_url='https://github.com/KTSStudio/tornkts/tarball/v' + version,

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='tornkts setuptools development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['tornado', 'torndsession', 'passlib', 'ujson']

)
