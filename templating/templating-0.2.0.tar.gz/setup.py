from distutils.core import setup

setup(
    name='templating',
    version='0.2.0',
    packages=['templating'],
    url='https://github.com/andir/templating',
    license='GPLv3',
    author='Andreas Rammhold',
    author_email='andreas@rammhold.de',
    description='Configurable templating of files.',
    entry_points={
      'console_scripts': [
          'templating = templating:main',
      ],
    },
    install_requires=[
        'Jinja2',
        'PyYAML',
        'jsonschema',
    ]
)
