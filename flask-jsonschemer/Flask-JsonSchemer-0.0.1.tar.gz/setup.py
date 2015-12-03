"""
Flask-JsonSchemer
----------

A Flask extension for validating JSON requets with jsonschema

"""
from setuptools import setup


setup(
    name='Flask-JsonSchemer',
    version='0.0.1',
    url='https://github.com/juztin/flask-jsonschemer',
    license='MIT',
    author='Matt Wright, Justin Wilson',
    author_email='matt@nobien.net, jsonschemer@minty.io',
    description='Flask extension for validating JSON requets',
    long_description=__doc__,
    py_modules=['flask_jsonschemer'],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'jsonschema>=2.5.1'
    ],
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
