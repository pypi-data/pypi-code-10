# coding=utf8
from setuptools import setup
__author__ = 'hellflame'


setup(
    name='paramSeeker',
    version="0.0.1",
    keywords=('param', 'parameter', 'terminal', 'handler'),
    description="终端参数获取、执行、",
    license='Apache License',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/paramSeeker",
    packages=[
        'paramSeeker'
    ],
    platforms="linux, mac os",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'seeker=paramSeeker.example:test_env'
        ]
    }
)


