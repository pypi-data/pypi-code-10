from setuptools import setup, find_packages

version = "0.2.1"

setup(
    name="argutils",
    packages=find_packages(),
    version=version,
    author='Erik Clarke',
    author_email='ecl@mail.med.upenn.edu',
    url='https://github.com/eclarke/argutils',
    description='Functions to build matched argument parsers and config files',
    long_description=open('README.rst').read(),
    install_requires=[
    	'six',
    	'pyyaml'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    license='GPLv2+'
)
