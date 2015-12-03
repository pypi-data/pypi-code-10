import os
from setuptools import setup, find_packages

ROOT = os.path.abspath(os.path.dirname(__file__))


setup(
    name='django-csrf-session',
    version='0.6.1',
    description='CSRF protection for Django without cookies.',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    author='Jeff Balogh',
    author_email='jbalogh@mozilla.com',
    maintainer='Matt Molyneaux',
    maintainer_email='moggers87+git@moggers87.co.uk',
    url='http://github.com/moggers87/django-csrf-session',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
