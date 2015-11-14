from setuptools import setup, find_packages



classifiers = []
with open("classifiers.txt") as fd:
    classifiers = fd.readlines()


setup(
    name="drivedroid-gen-repo",
    version="0.2.3",
    description="Generator for drivedroid repository files",
    author="Felix Richter",
    author_email="github@syntax-fehler.de",
    url="http://github.com/makefu/drivedroid-repo-gen",
    license="wtfpl",
    classifiers=classifiers,
    packages=find_packages(),
    entry_points = {
        'console_scripts' :
        ['drivedroid-gen-repo = drivedroid_gen:main'],
    },
    install_requires=['docopt'],
)
