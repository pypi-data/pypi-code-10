from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='mclient',
    version='0.1.3',
    packages=['mclient'],
    url='https://github.com/rusenask/mirage-client',
    license='GPLv3',
    author='Karolis Rusenas',
    author_email='karolis.rusenas@gmail.com',
    keywords=['testing', 'cli', 'mirage', 'client'],
    description='CLI and Client library for Mirage external service virtualization',
    long_description=readme(),
    install_requires=[
        'docopt', 'requests', 'PyYAML'
    ],
    requires=['docopt', 'requests', 'PyYAML'],
    entry_points={
        'console_scripts': ['mirage=mclient.mclient:main'],
    }
)
