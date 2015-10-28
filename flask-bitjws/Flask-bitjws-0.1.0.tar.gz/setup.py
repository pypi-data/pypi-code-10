from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development :: Libraries",
]

setup(
    name='Flask-bitjws',
    version='0.1.0',
    packages=['flask_bitjws'],
    include_package_data=True,
    url='https://github.com/deginner/flask-bitjws',
    license='MIT',
    classifiers=classifiers,
    author='deginner',
    author_email='support@deginner.com',
    description='A Flask extension for bitjws authentication.',
    setup_requires=['pytest-runner'],
    install_requires=[
        "Flask",
        "bitjws",
    ],
    tests_require=['pytest', 'pytest-cov']
)

