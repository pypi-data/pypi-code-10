import os
import re
from setuptools import setup


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()


setup(
	name='quickstartlog',
	version=__import__('quickstartlog').__version__,
    description='A simple log utility for building application quickly',
    long_description=readme,
    author='Sun Jin',
    author_email='sunjinopensource@qq.com',
    url='https://github.com/sunjinopensource/quickstartlog/',
	py_modules=['quickstartlog'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
