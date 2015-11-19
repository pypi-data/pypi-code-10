from pathlib import Path
from setuptools import setup

here = Path(__file__).parent
with here.joinpath('README.rst').open(encoding='utf-8') as f:
    README = f.read()
with here.joinpath('CHANGES.rst').open(encoding='utf-8') as f:
    CHANGES = f.read()
with here.joinpath('version.txt').open(encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name="metapensiero.odt2sphinx",
    version=VERSION,
    description="An OpenDocument to Sphinx converter.",
    long_description=README + '\n\n' + CHANGES,
    author="Christophe de Vienne",
    author_email="<cdevienne@gmail.com>",
    maintainer="Lele Gaifax",
    maintainer_email="lele@metapensiero.it",
    url='https://bitbucket.org/lele/metapensiero.odt2sphinx',
    install_requires=['Pillow'],
    extras_require={'dev': ['metapensiero.tool.bump_version']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    packages=['metapensiero.odt2sphinx'],
    package_dir={'metapensiero.odt2sphinx': 'odt2sphinx'},
    namespace_packages=['metapensiero'],
    entry_points={
        'console_scripts': [
            'odt2sphinx = metapensiero.odt2sphinx.__main__:main'
        ]
    }
)
