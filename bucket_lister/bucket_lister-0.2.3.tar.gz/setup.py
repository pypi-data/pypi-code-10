from setuptools import setup, find_packages

setup(
    name = 'bucket_lister',
    packages = find_packages(),
    version = '0.2.3',
    description = 'List S3 buckets for an account',
    author = 'Chris Barr',
    author_email = 'chris.barr@ntlworld.com',
    url = 'https://github.com/chrisbarr/bilious-rutabaga',
    download_url = 'https://github.com/chrisbarr/bilious-rutabaga/tarball/0.1',
    keywords = ['aws', 's3'],
    classifiers = [],
    install_requires = ['boto>=2.38.0'],
)
