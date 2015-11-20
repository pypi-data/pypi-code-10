from distutils.core import setup

from setuptools import find_packages


setup(
    name='chotot_trans',
    version='1.0',
    # packages=['api', 'api.v4', 'model', 'tests', 'appcore', 'fabfile', 'build.lib.chapy', 'build.lib.chapy.UAC',
    # 'build.lib.chapy.endpoints', 'build.bdist.macosx-10.10-x86_64.egg.chapy',
    # 'build.bdist.macosx-10.10-x86_64.egg.chapy.UAC', 'build.bdist.macosx-10.10-x86_64.egg.chapy.endpoints',
    #           'chapy', 'chapy.UAC', 'chapy.endpoints', 'tools.util', 'tools.util.test', 'api', 'api.v1', 'model',
    #           'tests', 'appcore', 'api', 'api.v1', 'model', 'tests', 'appcore', 'aria', 'hydra', 'api', 'api.v1',
    #           'model', 'appcore', 'api', 'api.v1', 'model', 'tests', 'appcore', 'proc', 'Rova', 'model', 'routes',
    #           'routes', 'routes'],
    packages=find_packages(),
    scripts=[
        "trans.py"
    ],
    package_data={
        '': ['*.py', '*.pyc', '*.pyx', '*.bconf', '*.txt']
    },
    url='http://chotot.vn',
    license='',
    author='Tan Tran',
    author_email='tantran@chotot.vn',
    description=''
)
