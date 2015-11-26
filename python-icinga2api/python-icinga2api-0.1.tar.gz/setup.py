from setuptools import setup, find_packages

PACKAGE = "icinga2api"
NAME = "python-icinga2api"
DESCRIPTION = "python icinga2 api "
AUTHOR = "fmnisme"
AUTHOR_EMAIL = "fmnisme@gmail.com"
URL = "http://my.oschina.net/fmnisme/blog"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(),
    zip_safe=False,
)