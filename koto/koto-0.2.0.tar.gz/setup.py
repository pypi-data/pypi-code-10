from setuptools import find_packages, setup

dependencies = ['docopt']

setup(
    name='koto',
    version='0.2.0',
    url='https://github.com/shukmeister/koto',
    license='MIT',
    author='Ben Shukman',
    author_email='shukipost@gmail.com',
    description='Command line email tracking',
    long_description=__doc__,
    packages=find_packages(),
    package_data={'':[]},
    include_package_data=False,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
          'koto=koto.koto:main' #what dis? originally: 'find_email=find_email.find_email:main'
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
          'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)