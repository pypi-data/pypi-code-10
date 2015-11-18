import os
import re

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), 'fnny', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), 'README.rst')


setup(
    name='fnny',
    version=VERSION,
    description="Hot function generators",
    long_description=open(readme).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='functional programming higher-ordered',
    author='Conrad Dean',
    author_email='conrad.p.dean@gmail.com',
    license='MIT',
    packages=['fnny'],
    include_package_data=True,
    tests_require=['py.test'],
    zip_safe=False,
)
