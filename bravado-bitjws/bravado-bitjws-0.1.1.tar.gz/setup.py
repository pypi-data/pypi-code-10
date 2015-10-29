from setuptools import setup
import bravado_bitjws

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="bravado-bitjws",
    version='0.1.1',
    description="Library for accessing Swagger-enabled API's with bitjws authentication.",
    author='Ira Miller',
    author_email='ira@deginner.com',
    url="https://github.com/deginner/bravado-bitjws",
    license='MIT',
    classifiers=classifiers,
    include_package_data=True,
    packages=["bravado_bitjws"],
    setup_requires=['pytest-runner'],
    install_requires=[
        "bravado-core >= 3.0.2",
        "pyasn1 >= 0.1.9",
        'secp256k1==0.11',
        "bitjws==0.6.3.1"
    ],
    tests_require=['pytest', 'pytest-cov']
)
