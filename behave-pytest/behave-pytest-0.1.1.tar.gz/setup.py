import setuptools

setuptools.setup(
    name="behave-pytest",
    version="0.1.1",
    url="https://github.com/ribozz/behave-pytest",

    author="Alex Rudakov",
    author_email="ribozz@gmail.com",

    description="Integrates pytest asserts with behave",
    long_description='Small utility package to integrate pytest asserts into Behave project.',

    packages=setuptools.find_packages(),

    install_requires=['pytest', 'behave'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)