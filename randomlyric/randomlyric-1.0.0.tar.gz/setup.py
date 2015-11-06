from setuptools import setup

with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = "randomlyric",
    packages = ["randomlyric"],
    install_requires = ['beautifulsoup4', 'getlyrics'],
    entry_points = {
        "console_scripts": ['randomlyric = randomlyric.randomlyric:main']
        },
    version = "1.0.0",
    description = "Get a random lyric from a random song, and url to the rest of the lyrics",
    long_description = long_descr,
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    url = "https://github.com/blha303/randomlyric",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Multimedia :: Sound/Audio"
        ]
    )
