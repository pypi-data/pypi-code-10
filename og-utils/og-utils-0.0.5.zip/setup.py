import os
from setuptools import setup, find_packages

def read(fname):
    with open(fname) as fhandle:
        return fhandle.read()

def readMD(fname):
    # Utility function to read the README file.
    full_fname = os.path.join(os.path.dirname(__file__), fname)
    if 'PANDOC_PATH' in os.environ:
        import pandoc
        pandoc.core.PANDOC_PATH = os.environ['PANDOC_PATH']
        doc = pandoc.Document()
        with open(full_fname) as fhandle:
            doc.markdown = fhandle.read()
        return doc.rst
    else:
        return read(fname)

version = '0.0.5'
packages = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', 'data'])
required = [req.strip() for req in read('requirements.txt').splitlines() if req.strip()]
setup(
    name='og-utils',
    version=version,
    author='Matthew Seal',
    author_email='mseal@opengov.com',
    description='A batch of python utilities shared by python repositories at OpenGov',
    long_description=readMD('README.md'),
    install_requires=required,
    license='MIT',
    packages=packages,
    test_suite='tests',
    zip_safe=False,
    url='https://github.com/OpenGov/og-python-utils',
    download_url='https://github.com/OpenGov/og-python-utils/tarball/v' + version,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2 :: Only'
    ]
)
