from setuptools import find_packages, setup

import versioneer


setup(
    name='blueberrywsn',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A Bluetooth wireless sensor network',
    url='https://github.com/felipedau/blueberrywsn',
    author='Felipe Dau',
    author_email='dau.felipe@gmail.com',
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='bluetooth raspberry pi wireless sensor network',
    packages=find_packages(),
    install_requires=[
        'pybluez>=0.22',
        'pyserial>=2.7',
    ],
    entry_points={
        'console_scripts': [
            'blueberrywsn=blueberrywsn:main',
        ],
    },

)
