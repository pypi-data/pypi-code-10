from setuptools import setup

setup(name='python-wink',
      version='0.3',
      description='Access Wink devices via the Wink API',
      url='http://github.com/bradsk88/python-wink',
      author='Brad Johnson',
      author_email='bradsk88@gmail.com',
      license='MIT',
      install_requires=['requests>=2.0', 'mock'],
      packages=['pywink'],
      zip_safe=True)
