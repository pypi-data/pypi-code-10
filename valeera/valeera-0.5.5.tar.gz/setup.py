from setuptools import setup, find_packages


setup(
  name='valeera',
  description='Validator for district42 schema',
  version='0.5.5',
  url='https://github.com/nikitanovosibirsk/valeera',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42==0.5.5',
    'Delorean==0.5.0'
  ]
)
