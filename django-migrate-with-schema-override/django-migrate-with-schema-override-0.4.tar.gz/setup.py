from setuptools import setup

packages = [
    'cursor_override',
]

setup(
    name='django-migrate-with-schema-override',
    version=0.4,
    packages=packages,
    include_package_data=True,
    license='MIT',
    description='Override migrate command not to trip on tables with schema name provided via db_tables.',
    long_description=open('README.rst').read(),
    author='Ariel Cercado',
    author_email='ariel.cercado@gmail.com',
    url='https://github.com/acercado/django-migrate-with-schema-override',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
)
