import os
from ez_setup import use_setuptools
use_setuptools(to_dir='/tmp')
from setuptools import setup, find_packages, findall


version = '0.1.1'
long_description = open('README.rst').read() + '\n\n' + open('CHANGES').read()

HERE = os.path.abspath(os.path.dirname(__file__))


def find_package_data():
    ignore_ext = {'.py', '.pyc', '.pyo'}
    base_package = 'cykooz'
    package_data = {}
    root = os.path.join(HERE, base_package)
    for path in findall(root):
        if path.endswith('~'):
            continue
        ext = os.path.splitext(path)[1]
        if ext in ignore_ext:
            continue

        # Find package name
        package_path = os.path.dirname(path)
        while package_path != root:
            if os.path.isfile(os.path.join(package_path, '__init__.py')):
                break
            package_path = os.path.dirname(package_path)
        package_name = package_path[len(HERE) + 1:].replace(os.path.sep, '.')

        globs = package_data.setdefault(package_name, set())
        data_path = path[len(package_path) + 1:]
        data_glob = os.path.join(os.path.dirname(data_path), '*' + ext)
        globs.add(data_glob)
    for key, value in package_data.items():
        package_data[key] = list(value)
    return package_data


setup(
    name='cykooz.buildout.basicauth',
    version=version,
    author='Alex Holmes',
    author_email='alex@alex-holmes.com',
    maintainer='Kirill Kuzminykh',
    maintainer_email='saikuz@mail.ru',
    url='https://bitbucket.org/cykooz/cykooz.buildout.basicauth',
    zip_safe=False,
    description='Buildout extension providing basic authentication support',
    long_description=long_description,
    license='Apache Public License',
    keywords='buildout basicauth http authentication',
    package_dir={'': '.'},
    packages=find_packages(),
    package_data=find_package_data(),
    namespace_packages=['cykooz', 'cykooz.buildout'],
    install_requires=[
        'setuptools',
        'six',
        'zc.buildout',
    ],
    extras_require={
        'test': ['mock', 'keyring'],
    },
    entry_points={
        'zc.buildout.extension':
            [
                'default = cykooz.buildout.basicauth:install',
            ],
    },
)
