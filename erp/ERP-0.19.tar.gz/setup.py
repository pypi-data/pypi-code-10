import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='ERP',
    version='0.19',
    packages=['erp', 'erp.base', 'erp.base.planning', 'erp.base.enterprise', 'erp.base.directory',
              'erp.base.storage', 'erp.base.article', 'erp.derivative', 'erp.derivative.trading', 'erp.extras'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/CLTanuki/ERP',
    license='BSD License',
    author='CLTanuki',
    author_email='CLTanuki@gmail.com',
    description='Resource Planning System',
    long_description=README,
    install_requires=['django', 'django-enumfield'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 3 - Alpha',
    ],
)