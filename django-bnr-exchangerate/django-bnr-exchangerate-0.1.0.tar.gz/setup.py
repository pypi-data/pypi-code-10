from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()
setup(
    name='django-bnr-exchangerate',
    version='0.1.0',
    packages=['bnr_exchangerate'],
    url='https://github.com/opencbsoft/django-bnr-exchangerate',
    license='MIT',
    author='Cristian Boboc',
    author_email='cristi@pidginhost.com',
    description='A django application to help with exchangerates from bnr.ro',
    long_description=long_description,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='exchangerate, bnr',
)
