from distutils.core import setup

setup(
    name='TowelStuffTest2',
    version='0.1.10',
    author='navforpython',
    author_email='navforpython@gmail.com',
    packages=['towel_stuff', 'towel_stuff.test'],
    scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/TowelStuffTest2/',
    license='LICENSE.txt',
    description='Useful towel-related stuff.',
    long_description=open('README.txt').read(),
)
