import setuptools


install_requires = [
    'lxml>=3.4.4',
    'mypy-lang>=0.2.0',
]


def readme() -> str:
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    name='docio',
    version='0.0.1',
    packages=setuptools.find_packages(),
    description="Extract / Swap text from several file formats.",
    long_descriptiondescription=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    license='GPLv3',
    author='Motoki Naruse',
    author_email='motoki@naru.se',
    url='https://github.com/yparrot/docio',
    keywords='text extract swap document doc',
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': [
            'pytest>=2.8.2',
            'pytest-xdist>=1.13.1',
            'pytest-cov>=2.2.0',
            'flake8>=2.5.0',
        ],
    }
)
