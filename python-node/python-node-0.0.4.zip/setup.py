from setuptools import setup
import pynode

setup(
    name='python-node',
    version=pynode.__version__,
    packages=[
        'pynode',
        'pynode.hosting_models',
        'pynode.runners'
    ],
    install_requires=[
        'psutil',
        'Naked',
        'requests',
    ],
    description='A node.js script runner for python',
    long_description='A node.js script runner. A full description can be found at https://github.com/ptMuta/python-node',
    author='Joona Romppanen',
    author_email='joona.romppanen@gmail.com',
    url='https://github.com/ptMuta/python-node',
)
