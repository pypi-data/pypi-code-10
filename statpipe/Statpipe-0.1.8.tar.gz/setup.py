from distutils.core import setup

setup(
    name='Statpipe',
    version='0.1.8',
    author='Ben Whalley',
    author_email='benwhalley@gmail.com',
    packages=['statpipe'],
    scripts=['bin/statpipe', 'bin/statpipe_image'],
    url='http://pypi.python.org/pypi/statpipe/',
    license='LICENSE.txt',
    description='Pipe stuff to Stata, get results back.',
    long_description=open('README.rst').read(),
    install_requires=['clint', ],
)
