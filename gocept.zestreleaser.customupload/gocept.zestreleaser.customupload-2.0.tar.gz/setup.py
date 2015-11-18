# See also LICENSE.txt

from setuptools import setup, find_packages

description = ("Plug-in for zest.releaser to allow uploading the created egg "
               "via SCP to configurable destinations.")

setup(
    name='gocept.zestreleaser.customupload',
    version='2.0',
    author='gocept gmbh & co. kg',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/gocept.zestreleaser.customupload',
    description=description,
    long_description="\n\n".join([open('COPYRIGHT.txt').read(),
                                  open('README.rst').read(),
                                  open('CHANGES.rst').read()]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL',
    namespace_packages=['gocept', 'gocept.zestreleaser'],
    install_requires=[
        'setuptools',
        'six',
        'zest.releaser >= 5.0',
    ],
    extras_require=dict(test=[
        'mock',
    ]),
    entry_points={
        'zest.releaser.releaser.after':
            ['upload=gocept.zestreleaser.customupload.upload:upload',
             'upload_doc=gocept.zestreleaser.customupload.doc:upload']},
)
