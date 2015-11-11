from setuptools import setup, find_packages

setup(
    name="Releasy",
    version="0.1",
    packages=find_packages(),
    scripts=[
        'scripts/releasy'
    ],
    author="Andre da Palma",
    author_email="andrefsp@gmail.com",
    url="https://github.com/andrefsp/releasy/",
    description="Releasy its a release notes manager for your projects",
    keywords = ['git', 'management', 'release'],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    requires=['gitpython(==1.0.1)'],
    install_requires=[
      'gitpython==1.0.1'  ,
    ]
)
