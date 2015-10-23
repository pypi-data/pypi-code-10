from distutils.core import setup
from mclient.mclient import version

setup(
    name='mclient',
    version="0.1",
    packages=['mclient'],
    url='https://github.com/rusenask/mirage-client',
    license='GPLv3',
    author='Karolis Rusenas',
    author_email='karolis.rusenas@gmail.com',
    keywords=['testing', 'cli', 'mirage', 'client'],
    description='CLI and Client library for Mirage external service virtualization',
    requires=['docopt', 'requests', 'PyYAML']
)
