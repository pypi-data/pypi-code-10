from setuptools import setup, find_packages

import python_field

setup(
    name = "python_field",
    version = python_field.__version__,
    description = "Store python source code (syntax checked) in database.",
    url = "https://github.com/mwaaas/django-python-code-field.git",
    author = "Chris Spencer",
    author_email = "chrisspen@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Environment :: Web Environment',
    ],
    zip_safe=True,
)
