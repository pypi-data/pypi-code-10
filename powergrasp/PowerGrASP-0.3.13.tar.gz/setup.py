# -*- coding: utf-8 -*-
#########################
#       SETUP.PY        #
#########################


#########################
# IMPORTS               #
#########################
from setuptools  import setup, find_packages
from powergrasp.info import __version__, __name__


#########################
# SETUP                 #
#########################
setup(
    name = __name__,
    version = __version__,

    packages = find_packages(),
    package_data = {
        'powergrasp': ['ASPsources/*.lp', 'logs/README.txt',
                       'tests/*.lp', 'tests/*.sbml', 'tests/*.gml'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyasp', 'docopt'],

    author = "lucas bourneuf",
    author_email = "lucas.bourneuf@openmailbox.org",
    description = "Graph compression with Answer Set Programming",
    long_description = open('README.mkd').read(),
    keywords = "graph",
    url = "https://github.com/Aluriak/powergrasp",

    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: ASP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)



