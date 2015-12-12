import os

from setuptools import setup


#from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="vhm-client",
    version="0.3.5",
    author="Pavel Studenik",
    author_email="studenik@varhoo.cz",
    description=("Client for manage systems and projects."),
    license = "GPL",
    keywords = "Client for Varhoo manager",
    url = "https://github.com/Pajinek/vhm",
    packages=['vhmlib', ],
    scripts=["vhm_check.py", "vhmcli.py"],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=["psutil", "requests" ],
    extras_require={
        "psutil": "python-psutil",
        "requests": "python-requests",
    }
)
