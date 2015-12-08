from setuptools import setup

setup(
  name = 'roadwarrior',
  version = '0.0.2',
  description = 'Tool for working remotely on large code bases.',
  url = 'https://github.com/denniskempin/roadwarrior',
  author = 'Dennis Kempin',
  author_email = 'dennis.kempin@gmail.com',
  license = 'MIT',
  py_modules = ['roadwarrior'],
  entry_points = {
    'console_scripts': [
      'roadwarrior=roadwarrior:main'
    ],
  }
)
