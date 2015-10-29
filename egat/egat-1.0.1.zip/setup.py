#####################################################################################
#
# To build the package and upload to PyPi
#    python setup.py sdist upload --sign
#
# To build and upload to Test PyPi
#    python setup.py sdist upload -r https://testpypi.python.org/pypi
# To install from Test PyPi
#    pip install -i https://testpypi.python.org/pypi egat
#
#####################################################################################
import setuptools
from distutils.core import setup
setup(
    name = 'egat',
    packages = ['egat', 'egat.loggers', 'egat.scripts'], # this must be the same as the name above
    include_package_data=True,
    package_data = {
        'data': ['default.css', 'egat-header.png']
    },
    entry_points = {
        'console_scripts': ['egatest = egat.scripts.egatest:run']
    },
    version = '1.0.1',
    description = 'An automated testing toolkit',
    author = 'E-gineering LLC',
    author_email = 'eg.pypi@e-gineering.com', # contact email
    url = 'https://github.com/egineering-llc/egat', # url with information about the package
    download_url = 'https://github.com/egineering-llc/egat/tarball/1.0.1', # should be a url of the tarball
    keywords = ['testing', 'automated testing', 'functional testing'], # arbitrary keywords
    classifiers = [],
)
