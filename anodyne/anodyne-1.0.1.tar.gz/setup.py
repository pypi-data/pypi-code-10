import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, "README.md")) as _file:
    README = _file.read()

with open(os.path.join(here, "CHANGELOG")) as _file:
    CHANGES = _file.read()

with open(os.path.join(here, "VERSION")) as _file:
    VERSION = _file.read().rstrip("\n")

with open(os.path.join(here, "requirements", "core.txt")) as _file:
    REQUIREMENTS = [r.rstrip("\n") for r in _file.readlines()]
    TEST_REQUIREMENTS = REQUIREMENTS[:]

with open(os.path.join(here, "requirements", "test.txt")) as _file:
    TEST_REQUIREMENTS += [r.rstrip("\n") for r in _file.readlines()]


setup(
    name="anodyne",
    description="SQLAlchemy Database Utilities",
    long_description=README + "\n\n" + CHANGES,
    packages=find_packages(exclude=["tests"]),
    version=VERSION,
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    maintainer="Alex Milstead",
    maintainer_email="alex@amilstead.com",
    url="https://github.com/amilstead/anodyne",
    keywords=["sqlalchemy"],
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Database ",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
)
