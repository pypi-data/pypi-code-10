"""
see: http://python-packaging-user-guide.readthedocs.org/en/latest/distributing
see: https://youtu.be/kNke39OZ2k0?t=47
"""

from setuptools import setup, find_packages

setup(
    name='ami-organizer',
    author='Sam Keen',
    author_email='sam.sjk@gmail.com',
    url='https://github.com/samkeen/ami-organizer',
    download_url='https://github.com/samkeen/ami-organizer/archive/v0.1.0.tar.gz',
    version='v0.1.0',
    description='An AMI creator and cataloging system',
    keywords=['ami', 'aws', 'ec2'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'Topic :: Utilities',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    # py_modules=['amiorganizer'],
    install_requires=[
        'Click',
        'pytz',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'amiorganizer=amiorganizer.application:main'
        ]
    },

)
