from setuptools import setup


setup(
    name='Flask-Babeled',
    version='0.9.3',
    url='http://github.com/jeremyosborne/flask-babeled',
    license='BSD',
    author='Armin Ronacher, Jeremy Osborne',
    author_email='armin.ronacher@active-4.com, jeremywosborne@gmail.com',
    description='Adds i18n/l10n support to Flask applications',
    long_description=open("README.md").read(),
    packages=['flask_babeled'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Babel>=1.0',
        'speaklater>=1.2',
        'Jinja2>=2.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
