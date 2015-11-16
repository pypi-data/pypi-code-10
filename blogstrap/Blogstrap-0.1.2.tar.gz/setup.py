"""A dumb blogging platform based on Strapdown.js
"""

from setuptools import setup

repo_url="http://github.com/joehakimrahme/blogstrap"

setup(
    name='Blogstrap',
    author="Joe H. Rahme",
    author_email="joehakimrahme@gmail.com",
    version='0.1.2',
    description="A dumb blogging platform based on Strapdown.js",
    url=repo_url,
    download_url=repo_url + "/tarball/0.1.2",
    long_description=__doc__,
    packages=['blogstrap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
