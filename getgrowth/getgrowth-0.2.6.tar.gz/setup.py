from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

#NOTE: Other stuff to install
#Windows: GTK+ all-in-one bundle and binaries for numpy/scipy
#OS X: 
#Ubuntu: sudo apt-get python-gtk2-dev python-gtk2 libfreetype6-dev libpng-dev

setup(name='getgrowth',
      version='0.2.6',
      description='Determining growth rates from Biolector experiments',
      url='http://github.com/rasmusagren/getgrowth',
      author='Rasmus Agren',
      author_email='rasmus@alembic.se',
      license='GNU General Public License v2.0',
      packages=['getgrowth'],
      include_package_data=True,
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'statsmodels'],
      zip_safe=False)