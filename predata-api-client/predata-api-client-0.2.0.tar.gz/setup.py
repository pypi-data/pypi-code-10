from setuptools import setup

setup(
    name='predata-api-client',
    version='0.2.0',
    description='Predata Python API Client',
    author='predata',
    author_email='dev@predata.com',
    url='http://www.predata.com',
    packages=["predata", "predata/helpers", "predata/config"],
    install_requires=[
        "requests==2.5.1",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
