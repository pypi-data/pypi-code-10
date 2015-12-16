from distutils.core import setup
setup(
  name = 'pyfacebook',
  packages = ['pyfacebook'], # this must be the same as the name above
  version = '0.3',
  description = 'A facebook library with classes for various facebook stuff',
  author = 'Stefan Nozinic',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/pyfb', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/pyfb/tarball/0.3',
  keywords = ['facebook', 'chat'], # arbitrary keywords
  classifiers = [],
  install_requires=["facepy"]
)
