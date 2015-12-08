from distutils.core import setup

setup(
    name='serpentologist',
    packages=['serpentologist'],
    package_dir={'': 'src'},
    version='0.0.1a1',
    # TODO
    description='A Python library for carefully refactoring critical paths. inspired by https://github.com/github/scientist',
    author='Jacques-Olivier D. Bernier',
    author_email='jdesjardinsbernier@gmail.com',
    url='https://github.com/jackdbernier/serpentologist',
    # TODO
    keywords=['testing', 'benchmark', 'monitoring'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
