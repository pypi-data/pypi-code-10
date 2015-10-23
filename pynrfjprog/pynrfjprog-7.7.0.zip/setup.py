

from setuptools import setup, find_packages

import sys
py2 = sys.version_info[0] == 2
py3 = sys.version_info[0] == 3

if py2:
    requirements = ['enum34', 'future']
elif py3:
    requirements = ['future']

import pynrfjprog

setup(
    
    name ='pynrfjprog',
        
    version = pynrfjprog.__version__,
    
    description = 'A simple Python interface for the nrfjprog.dll',
    long_description = 'A simple Python interface for the nrfjprog.dll. Since nrfjprog.dll is a 32 bit windows application, this package can only be used with windows and 32bit Python 2.7.x',
    
    url = 'http://www.nordicsemi.com/',
        
    author = 'Nordic Semiconductor ASA',
    
    license = 'BSD',
    
    classifiers = [

        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    
    keywords = 'nrfjprog pynrfjprog',
     
    install_requires = requirements,
     
    packages = find_packages(),
    package_data = { 
                'pynrfjprog': ['*.dll', '*.so'],
                'pynrfjprog.docs': ['*.h'],
                'pynrfjprog.examples': ['*.hex']
    }
    
    )