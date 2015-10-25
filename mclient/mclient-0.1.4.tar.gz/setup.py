from setuptools import setup
from mclient.mclient import version


setup(
    name='mclient',
    version=version,
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
    }
)
