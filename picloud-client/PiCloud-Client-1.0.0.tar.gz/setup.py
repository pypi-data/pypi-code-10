from distutils.core import setup

setup(
    name='PiCloud-Client',
    version='1.0.0',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['picloud_client'],
    url='https://github.com/exitcodezero/picloud-client-python',
    license='LICENSE.txt',
    description='A Python client for PiCloud',
    long_description=open('README.txt').read(),
    install_requires=[
        "websocket-client == 0.32.0",
    ],
)
