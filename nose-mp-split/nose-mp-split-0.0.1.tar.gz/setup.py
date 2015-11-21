import setuptools

long_description = open('README.rst').read()

VERSION = '0.0.1'

setup_params = dict(
    name='nose-mp-split',
    version=VERSION,
    author='Paul Glass',
    author_email='pnglass@gmail.com',
    url='https://github.com/pglass/nose-mp-split',
    keywords='nose parallel multiprocess concurrency split',
    packages=setuptools.find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={'nosempsplit': 'nosempsplit'},
    include_package_data=True,
    description='an improved multiprocess plugin for nose',
    long_description=long_description,
    install_requires=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'mp-split = nosempsplit.plugin:MpSplitPlugin',
        ],
    },
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
