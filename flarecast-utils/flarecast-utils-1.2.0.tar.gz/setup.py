from distutils.core import setup

try:
    import pypandoc

    description = pypandoc.convert('README.md', 'rst')
except:
    description = ''

setup(
    name='flarecast-utils',
    version='1.2.0',
    packages=['flarecast', 'flarecast.utils'],
    url='https://dev.flarecast.eu/stash/projects/INFRA/repos/utils/',
    license='',
    author='Florian Bruggisser',
    author_email='florian.bruggisser@students.fhnw.ch',
    description='Flarecast utils provides tools to interact '
                'with the flarecast infrastructure.',
    long_description=description,
    download_url='https://dev.flarecast.eu/stash/scm/infra/utils.git',
    keywords=['flarecast', 'utils', 'esa', 'solar', 'weather', 'prediction'],
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)
