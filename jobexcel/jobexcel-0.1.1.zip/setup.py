try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='jobexcel',
    version='0.1.1',
    author='haibo',
    author_email='hbnnlong@163.com',
    description='haibo universal function',
    license='MIT',
    packages=['jobexcel',],
    install_requires=['xlwt>=1.0.0',
                      'xlrd>=0.9.4',
                      'xlutils>=1.7.1'
                      ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
    keywords='jobexcel function',
    url='hbnnlove.sinaapp.com',
    zip_safe=True,
    include_package_data=True,
    platforms='any'
)
