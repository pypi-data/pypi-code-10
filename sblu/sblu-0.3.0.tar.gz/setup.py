from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open("requirements.txt", "r") as requirements_file:
    requirements = [x.strip() for x in requirements_file.readlines()]

scripts = (
    'scripts/cl_load_job', 'scripts/cluspro_local.py',
    'scripts/cluster.py', 'scripts/ftrmsd.py')

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="sblu",
    version="0.3.0",
    packages=['sblu', 'sblu.cli'],
    description="Library for munging data files from ClusPro/FTMap/etc.",
    long_description=long_description,
    url="https://bitbucket.org/bu-structure/sb-lab-utils",
    author="Bing Xia",
    author_email="sixpi@bu.edu",
    license="MIT",
    install_requires=requirements,
    scripts=scripts,
    entry_points={
        'console_scripts': [
            "sblu = sblu.cli:cli",
            # Prep commands
            "pdbclean = sblu.cli.prep:clean",
            "pdbsplitsegs = sblu.cli.prep:splitsegs",
            # RMSD commands
            "srmsd = sblu.cli.rmsd:srmsd",
            "pypwrmsd = sblu.cli.rmsd:pwrmsd",
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords='cluspro protein PDB',
    use_2to3=True, )
