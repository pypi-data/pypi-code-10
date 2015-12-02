from setuptools import setup
setup(
  name = 'py-readability',
  packages = ['pyreadability'], 
  version = '1.0',
  description = 'Calculate readability index values',
  author = 'Matt Selph',
  author_email = 'matt@mattselph.io',
  url = 'https://github.com/mattselph/readability', 
  download_url = 'https://github.com/mattselph/readability/tarball/1.0', 
  keywords = ['readability'],
  classifiers = [],
  install_requires=[
	'nltk',
	'num2words'
  ]
)
