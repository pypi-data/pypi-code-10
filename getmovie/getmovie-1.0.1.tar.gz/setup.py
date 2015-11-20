from setuptools import setup

with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = "getmovie",
    packages = ["getmovie"],
    install_requires = ['requests', 'prettytable'],
    entry_points = {
        "console_scripts": ['getmovie = getmovie.getmovie:main']
        },
    version = "1.0.1",
    description = "Look up movie from YTS",
    long_description = long_descr,
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    url = "https://github.com/blha303/getmovie/",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Multimedia :: Sound/Audio"
        ]
    )
