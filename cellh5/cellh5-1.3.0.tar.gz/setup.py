import setuptools

setuptools.setup(
    name="cellh5",
    version="1.3.0",
    description="A format for data exchange in high-content screening",
    long_description="A format for data exchange in high-content screening",
    url="http://cellh5.org",
    author="Christoph Sommer, Rudolf Hoefler",
    author_email="christoph.sommer@imba.oeaw.ac.at, rudolf.hoefler@gmail.com",
    license="LGPL",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering"
    ],
    keywords="",
    packages=setuptools.find_packages(
        exclude=[
            "*.test",
            "*.test.*",
            "test",
            "test.*"
        ]
    ),
    install_requires=[
        "h5py",
        "hmmlearn",
        "lxml",
        "matplotlib",
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy"
    ],
    package_data={
        "hmm_wrapper": [
            "hmm_constraint.xsd"
        ]
    },
    entry_points={
        "console_scripts": [

        ],
        "gui_scripts": [

        ]
    }
)
