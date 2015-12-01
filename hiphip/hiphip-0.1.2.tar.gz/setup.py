from setuptools import setup, find_packages


setup(
  name='hiphip',
  description='',
  version='0.1.2',
  url='https://github.com/nikitanovosibirsk/hiphip',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'requests>=2.2.1'
  ]
)
