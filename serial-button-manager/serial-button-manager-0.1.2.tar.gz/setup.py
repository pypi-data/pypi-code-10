#!/usr/bin/python
import os
from setuptools import setup, find_packages


requirements_path = os.path.join(
    os.path.dirname(__file__),
    'requirements.txt',
)
try:
    from pip.req import parse_requirements
    requirements = [
        str(req.req) for req in parse_requirements(requirements_path)
    ]
except Exception:
    requirements = []
    with open(requirements_path, 'r') as in_:
        requirements = [
            req for req in in_.readlines()
            if not req.startswith('-')
            and not req.startswith('#')
        ]


setup(
    name="serial-button-manager",
    version="0.1.2",
    description=(
        "Control whether or not a service is running with an "
        "easy-to-construct button connected to a serial port."
    ),
    author="Adam Coddington",
    author_email="me@adamcoddington.net",
    url="http://github.com/coddingtonbear/serial-button-manager",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'serial-button-manager = serial_button_manager.cmdline:main'
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
    ]
)
