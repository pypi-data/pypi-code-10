from setuptools import setup
from mclient import version

setup(
    name='mclient',
    packages=['mclient'],
    url='https://github.com/rusenask/mirage-client',
    license='GPLv3',
    author='Karolis Rusenas',
    author_email='karolis.rusenas@gmail.com',
    keywords=['testing', 'cli', 'mirage', 'client'],
    description='CLI and Client library for Mirage external service virtualization',
    install_requires=[
        'docopt', 'requests', 'PyYAML'
    ],
    requires=['docopt', 'requests', 'PyYAML'],
    entry_points={
        'console_scripts': ['mirage=mclient.mclient:main'],
    },
    version=version,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['nose'],
    },
)
