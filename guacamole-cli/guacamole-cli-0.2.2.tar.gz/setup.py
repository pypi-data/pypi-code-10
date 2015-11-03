from setuptools import setup, find_packages


setup(
    name="guacamole-cli",
    version="0.2.2",
    author="Pablo SEMINARIO",
    author_email="pablo@seminar.io",
    description="Guacamole command line interface",
    license="GNU General Public License v3 (GPLv3)",
    url="https://github.com/Antojitos/guacamole-cli",
    download_url="https://github.com/Antojitos/guacamole-cli/archive/0.2.2.tar.gz",
    keywords=["cli", "guacamole"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],

    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'guacamole = guacamole_cli:main',
        ]
    },
    install_requires=['requests'],
)
