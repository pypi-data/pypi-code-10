from distutils.core import setup
import pypandoc
#with open('README.rst') as f:  
#    long_description = f.read()
long_description = pypandoc.convert('README.md', 'rst')
setup(
  name = 'pythonversion',
  packages = ['pythonversion'], # this must be the same as the name above
  version = '0.2',
  description = 'Check Python version',
  long_description=long_description,
  author = 'Boying Xu',
  author_email = 'xuboying@gmail.com',
  license='MIT',
  url = 'https://github.com/xuboying/pythonversion/', # use the URL to the github repo
  download_url = 'https://github.com/xuboying/pythonversion/tarball/0.2', # I'll explain this in a second
  keywords = ['version'], # arbitrary keywords
  classifiers = ['Programming Language :: Python :: 2', 'Programming Language :: Python :: 3'],
)