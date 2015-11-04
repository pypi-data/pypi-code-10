import setuptools
from global_identity.version import Version

setuptools.setup(name='global_identity',
                 packages = ['global_identity'],
                 version=Version('0.1.0').number,
                 description='Global Identity Authentication PIP',
                 long_description='Global Identity Authentication PIP',
                 author='mralves',
                 author_email='mralves@stone.com.br',
                 url='http://github.com/MateusRA/globalidentity-python',
                 download_url = 'https://github.com/MateusRA/globalidentity-python/tarball/v0.0.1',
                 py_modules=['global_identity'],
                 install_requires=['requests'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='global identity',
                 classifiers=[])
