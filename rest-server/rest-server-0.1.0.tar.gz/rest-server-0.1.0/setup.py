from distutils.core import setup

setup(
    name='rest-server',
    version='0.1.0',
    url="http://github.io/boundary/rest-server",
    author='David Gwartney',
    author_email='david_gwartney@bmc.com',
    packages=['restserver', ],
    scripts=[
    ],
    package_data={'restserver': ['templates/*']},
    license='LICENSE',
    description='TrueSight Pulse Meter Plugin SDK for Python',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask >= 0.10.1"
    ],
)
