from setuptools import setup

VERSION = "1.0.3"

setup(
    name="melt",
    py_modules=['melting'],
    version=VERSION,
    author='Erik Clarke',
    author_email='ecl@mail.med.upenn.edu',
    url='https://github.com/eclarke/melt',
    description='A nucleotide melt temp calculator',
    long_description=open('README.rst').read(),
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'        
    ],
    license='GPL 3',
    entry_points={'console_scripts': ['Tm = melting:main']}
)
