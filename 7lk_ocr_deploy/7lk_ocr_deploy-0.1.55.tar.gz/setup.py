# -*- coding: utf-8 -*-
import codecs
import os
import sys

from setuptools import find_packages
from distutils.core import setup, Extension

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "7lk_ocr_deploy"
"""
名字，一般放你包的名字即可
"""

PACKAGES = ["libsvm", ]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "Some deploy packages for ocr."

LONG_DESCRIPTION = read("README.txt")

KEYWORDS = "test python package"

AUTHOR = "cjyfff"

AUTHOR_EMAIL = "youremail@email.com"


URL = "http://blog.useasp.net/"


VERSION = "0.1.55"


LICENSE = "MIT"

# from subprocess import call
# from setuptools.command.install import install
#
#
# class MyInstall(install):
#     def run(self):
#         # call(["tar zxvf ./libsvm/libsvm.tar.gz"], shell=True)
#         install.run(self)


svm = Extension('libsvm', sources=['libsvm-source/svm.cpp'], library_dirs=['/usr/local/lib'],)
svm_predict = Extension('svm-predict', sources=['libsvm-source/svm-predict.c'])
svm_scale = Extension('svm-scale', sources=['libsvm-source/svm-scale.c'])
svm_train = Extension('svm-train', sources=['libsvm-source/svm-train.c'])


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    ext_modules=[svm, svm_predict, svm_scale, svm_train]
    # cmdclass={'install': MyInstall},
    # package_data={'libsvm': ['libsvm.tar.gz'], },
)
