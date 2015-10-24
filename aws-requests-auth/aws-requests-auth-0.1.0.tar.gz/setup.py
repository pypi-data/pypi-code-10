from distutils.core import setup


setup(
    name='aws-requests-auth',
    version='0.1.0',
    author='David Muller',
    author_email='davehmuller@gmail.com',
    packages=['aws_requests_auth'],
    url='https://github.com/davidmuller/aws-requests-auth',
    license='LICENSE.txt',
    description='AWS signature version 4 signing process for the python requests module',
    long_description=open('README.md').read(),
    install_requires=['requests>=0.14.0'],
)
