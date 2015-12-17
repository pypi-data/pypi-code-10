from setuptools import setup

setup(
    name='py-protocols',
    description='Absraction separation tool for python. Inspired by clojure protocols',
    license='MIT',
    version='1.0.0',
    author='Vojta Orgon',
    author_email='villlem@gmail.com',
    url='https://github.com/villlem/py-protocols',
    packages=['py_protocols'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)