# -*- coding: utf-8 -*-

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

kwargs = {}

with open('README.rst') as f:
    kwargs['long_description'] = f.read()

if setuptools is not None:
    # 添加相关依赖
    install_requires = ['requests']
    # install_requires.append('requests')
    kwargs['install_requires'] = install_requires

setup(
    name="ebcloudstore",
    packages=["ebcloudstore"],
    version="1.1",
    description="nullpa cloud store",
    author="zdw",
    author_email="zhengdw@56iq.com",
    url="http://open.53iq.com/guide",
    keywords=["53iq", "xingji", "ebanswers"],
    license="http://www.apache.org/licenses/LICENSE-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
    ],
    **kwargs
)