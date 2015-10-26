import os
from setuptools import setup, find_packages


VERSION = '0.0.2'

install_requires = [
]

here = os.path.dirname(os.path.abspath(__file__))
# get documentation from the README and HISTORY
try:
    with open(os.path.join(here, 'README.rst')) as doc:
        readme = doc.read()
except:
    readme = ''

try:
    with open(os.path.join(here, 'HISTORY.rst')) as doc:
        history = doc.read()
except:
    history = ''

long_description = readme + '\n\n' + history


if __name__ == '__main__':
    setup(
          name='presentation_api_controller',
          version=VERSION,
          description='Presentation API Controller for MCTS',
          long_description=long_description,
          keywords='mozilla b2g firefoxos fxos MCTS ',
          author='Askeing Yen',
          author_email='askeing@gmail.com',
          url='https://github.com/askeing/presentation_api_controller',
          packages=find_packages(exclude=['ez_setup', 'examples']),
          package_data={},
          install_requires=install_requires,
          zip_safe=False,
  )
