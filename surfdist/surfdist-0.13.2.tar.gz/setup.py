from distutils.core import setup
setup(
  name = 'surfdist',
  packages = ['surfdist'],
  install_requires = ['numpy',                                              
                      'mayavi',                        
                      'gdist', 
                      'nibabel',
                      'os>=10.1',
                      'scipy'],
  version = '0.13.2',
  description = 'For calculating exact geodesic distances on cortical surface meshes',
  author = 'Daniel Margulies',
  author_email = 'margulies@cbs.mpg.de',
  url = 'https://github.com/margulies/surfdist',
  download_url = 'https://github.com/margulies/surfdist/tarball/0.13.2',
  keywords = ['geodesic', 'distance', 'brain', 'cortex'],
  classifiers = [],
)
