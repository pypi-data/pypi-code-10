# coding=utf8

from setuptools import setup, find_packages
import demo_pkg_lfr

setup(
    name="demo_pkg_lfr",
    version=demo_pkg_lfr.__version__,
    packages=find_packages(),
    author="Moi",
    author_email="spam@yopmail.com",
    description="Librairie de démo",
    long_description=open("README.md").read(),
    include_package_data=True,
    url="http://perdu.com",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ],
    entry_points = {
        'console_scripts' : [
            "demo-pkg-lfr-hello = demo_pkg_lfr:hello"
        ]
    }
)