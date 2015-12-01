from distutils.core import setup

setup(
    name='flask-morepath',
    version='0.1',
    packages=['flask_morepath'],
    url='',
    license='MIT',
    author='Alexander Plavin',
    author_email='alexander@plav.in',
    description='',
    install_requires=[
        'cached-property',
        'flask',
        'flask-mako',
    ],
)
