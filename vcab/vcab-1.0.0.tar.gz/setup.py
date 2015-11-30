from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

setup(
    name = "vcab",
    version = "1.0.0",
    description = "Bridge tool to connect VCP and absinthe",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/vcab.git',
    license = 'MIT',
    install_requires = [
        "vcp>=1.4.0",
        "absinthe>=1.1.0",
        "voidpp-tools>=1.1.1",
        "Flask-uWSGI-WebSocket>=0.5.0",
    ],
    packages = find_packages(),
    scripts = [
    ],
)
