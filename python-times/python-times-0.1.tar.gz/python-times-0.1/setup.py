from setuptools import setup, Extension
setup(
    name="python-times",
    version="0.1",
    description="Get the real, user and system time consumed by your Python program",
    author="Pau Freixes",
    author_email="pfreixes@gmail.com",
    url="https://github.com/pfreixes/python-times",
    ext_modules=[Extension("times", ["times.c"])]
)
