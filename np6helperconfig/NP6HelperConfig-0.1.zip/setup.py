from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='NP6HelperConfig',
      version='0.1',
	  description='get informations present on the config.ini or in an other file formated for a configparser',
      long_description=readme(),
      keywords='configparser informations configuration config',
      url='https://github.com/NP6/Python',
      author='NP6 -SpaghetTeam',
      author_email='fpi@np6.com',
      license='CC Licence',
      packages=['NP6HelperConfig'],
      zip_safe=False)