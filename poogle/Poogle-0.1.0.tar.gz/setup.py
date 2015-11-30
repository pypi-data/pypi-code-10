from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='Poogle',
    version='0.1.0',
    description='Poogle is a Google scraping library and command line utility for Python.',
    long_description=readme(),
    author='Makoto Fujimoto',
    author_email='makoto@makoto.io',
    url='https://github.com/FujiMakoto/Poogle',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
    keywords=['google', 'web search', 'search engine'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'poogle = poogle.cli:cli'
        ],
    },
    install_requires=['requests>=2.8.1,<2.9', 'click>=6.2,<6.3', 'beautifulsoup4>=4.4.1,<4.5', 'yurl>=0.13,<0.14'],
)
