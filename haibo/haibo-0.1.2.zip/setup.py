__author__ = 'BJHaibo'


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='haibo',
    version='0.1.2',
    author='haibo',
    author_email='hbnnlong@163.com',
    description='haibo universal function',
    license='MIT',
    packages=['haibo',],
    install_requires=['mako>=1.0.3',
                      ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
    keywords='haibo function',
    url='hbnnlove.sinaapp.com',
    zip_safe=True,
    include_package_data=True,
    platforms='any'
)
