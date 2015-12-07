from distutils.core import setup
setup(
  name = 'smackbone',
  packages = ['smackbone'],
  version = '0.0.2',
  description = 'Smackbone Client',
  author = 'Peter Bjorklund',
  author_email = 'piot@hotmail.com',
  url = 'https://github.com/piot/smackbone-python',
  download_url = 'https://github.com/Piot/smackbone-python/archive/v0.0.2.tar.gz',
  keywords = ['smackbone'],
  classifiers = [],
  install_requires = ['websocket-client>=0.34.0'],
)
