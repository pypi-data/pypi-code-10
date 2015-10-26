from setuptools import setup

setup(
    name = 'nginxctl',
    packages = ['nginxctl'],
    version = '1.0',
    description = 'This tool is similar to apachectl but for nginx. The \
                    important feature of this tool is ability to list vhosts \
                    configured on a nginx server',
    author='Alex Newton Alexander',
    author_email='fooltruth1980@gmail.com',
    url='https://github.com/fooltruth/nginxctl',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: Console',
    ]
)
