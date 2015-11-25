from distutils.core import setup

setup(
    name="un_iife_ize",
    version="1.0b2",
    description="Javascript potential IIFE remover",
    author="Yusaira Khan",
    author_email="yusaira.khan@mail.mcgill.ca",

    scripts=["un_iife_ize.py"],

    url="https://github.com/AmiApp/un_iife_ize",
    download_url="https://github.com/AmiApp/un_iife_ize/archive/1.0b2.tar.gz",
    keywords=["javascript", "iife", "remove"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    long_description="""\
Javascript Potential IIFE removal
-------------------------------------

Variable declarations done properly in javascript files look like IIFEs to MeteorJS.
This script converts


Requires Python 3 or later
"""
)
