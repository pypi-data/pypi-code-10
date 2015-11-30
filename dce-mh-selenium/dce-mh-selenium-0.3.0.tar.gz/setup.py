
import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(path):
    return codecs.open(os.path.join(here, path), 'r', 'utf-8').read()

readme = read('README.md')
history = read('HISTORY.md')
version_file = read('mh_selenium/__init__.py')
version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M).group(1)

install_requires = [
    "selenium==2.47.1",
    "click==5.1",
    "fabric==1.10.2",
    "pytimeparse==1.1.5",
    "unipath==1.1",
]

setup(
    name='dce-mh-selenium',
    version=version,
    packages=find_packages(),
    url='https://github.com/harvard-dce/mh-selenium',
    license='Apache 2.0',
    author='Jay Luker',
    author_email='jay_luker@harvard.edu',
    description='Selenium tasks and page objects for DCE Matterhorn',
    long_description=readme + '\n\n' + history,
    install_requires=install_requires,
    py_modules=["mh_driver", "mh_selenium"],
    entry_points='''
        [console_scripts]
        mh_driver=mh_driver:cli
    '''
)
