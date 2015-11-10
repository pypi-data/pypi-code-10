# It's a fast fix for http://hg.python.org/cpython/rev/0a58fa8e9bac
try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup, find_packages


setup_args = dict(name='sergelab.utils',
                  version='0.11',
                  author='Alexey Slynko, Sergey Syrov',
                  author_email='info@sergelab.ru',
                  url='https://bitbucket.org/serge_brpr/sergelab.utils/',
                  description='Python utilities',
                  long_description=open('README.rst').read(),
                  namespace_packages=['sergelab'],
                  install_requires=['distribute', 'nose'],
                  tests_require=['nose'],
                  test_suite='nose.collector',
                  packages=find_packages('.'),
                  package_dir={'': '.'},
                  zip_safe=True)


if __name__ == '__main__':
    setup(**setup_args)
