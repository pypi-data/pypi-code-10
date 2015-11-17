from distutils.core import setup
setup(
  name = 'asyncrest',
  modules = ['asyncrest'],
  version = '1.0',
  description = 'RESTful helper for asyncio',
  author = 'Kamyar Inanloo',
  author_email = 'kamyar1979@gmail.com',
  install_requires = ['asyncio','aiohttp'],
  url = 'https://bitbucket.org/kamyar1979/asyncrest',
  keywords = ['asyncio', 'rest', 'pep3156','aiohttp','restful'], 
  classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP'],
)