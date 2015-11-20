from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='getgrowth',
      version='0.2.5',
      description='Determining growth rates from Biolector experiments',
      url='http://github.com/rasmusagren/getgrowth',
      author='Rasmus Agren',
      author_email='rasmus@alembic.se',
      license='GNU General Public License v2.0',
      packages=['getgrowth'],
      include_package_data=True,
      install_requires=[
          'pandas>=0.17.0',
          'numpy>=1.8',
          'matplotlib>=1.5',
          'pygtk>=2.24.0',
          'statsmodels>=0.6.1'],
      zip_safe=False)