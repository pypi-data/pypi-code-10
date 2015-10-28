# -*- coding: utf-8 -*-
import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
"""
打包的用的setup必须引入，
"""


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

PACKAGES = ["libsvm", "my_test"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "Some deploy packages for ocr."
"""
关于这个包的描述
"""

LONG_DESCRIPTION = read("README.txt")
"""
参见read方法说明
"""

KEYWORDS = "test python package"
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""

AUTHOR = "cjyfff"
"""
谁是这个包的作者，写谁的名字吧
"""

AUTHOR_EMAIL = "youremail@email.com"
"""
作者的邮件地址
"""

URL = "http://blog.useasp.net/"
"""
你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
"""

VERSION = "0.1.45"
"""
当前包的版本，这个按你自己需要的版本控制方式来
"""

LICENSE = "MIT"
"""
授权方式，我喜欢的是MIT的方式，你可以换成其他方式
"""
from subprocess import call
from setuptools.command.install import install


class MyInstall(install):
    def run(self):
        call(["pip install Django"], shell=True)
        install.run(self)


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
    # package_data={'libsvm': ['*'],
    #               },
    # entry_points={
    #     'console_scripts': [
    #         'foo = my_test.command_line:main',
    #     ],
    # }
    # scripts=['bin/setup.py'],
    # data_files=[('my_data', ['libsvm/fuck'])],
    cmdclass={'install': MyInstall},
)

# os.system('mkdir -p ./my_test/fuck')
