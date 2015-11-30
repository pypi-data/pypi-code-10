import os
from setuptools import setup
from pip.req import parse_requirements
import kou.koucmd as app
import uuid


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='kou',
    version=app.__version__,
    author='Burak Köse',
    author_email='burakks41@gmail.com',
    description='Kocaeli University OBS Command Line Interface',
    url='https://github.com/burakkose/kou-obs-cli',
    license='The MIT License',
    packages=['kou'],
    platforms=['OS Independent'],
    keywords=['cli', 'kou', 'obs'],
    classifiers=[],
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    scripts=['bin/koucli'],
    install_requires=reqs,
)
