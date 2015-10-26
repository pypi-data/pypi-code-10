from setuptools import setup

setup(
    name='silentiary',
    version='0.1.0',
    author='Arthur Dick',
    author_email='arthur@arthurdick.com',
    description='Password manager',
    license='GPLv3',
    keywords='password',
    url='https://github.com/arthurdick/silentiary',
    scripts=['silentiary.py'],
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Security",
    ],
    test_suite="test_silentiary",
    install_requires=["docopt"],
    setup_requires=["docopt"],
)
