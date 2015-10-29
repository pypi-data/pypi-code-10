from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='NP6HelperHttp',
      version='0.1',
	  description='helper to analyze header Http',
      long_description=readme(),
      keywords='http header content-type NP6',
      url='https://github.com/NP6/Python',
      author='NP6 -SpaghetTeam',
      author_email='fpi@np6.com',
      license='CC Licence',
      packages=['NP6HelperHttp'],
      zip_safe=False)