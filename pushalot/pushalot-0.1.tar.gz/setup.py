from setuptools import (
    find_packages,
    setup,
)

setup(
    name='pushalot',
    install_requires=['six'],
    packages=find_packages(),
    version='0.1',
    description='Wrapper for pushalot.com service',
    author='Alex Bo',
    author_email='public@the-bosha.ru',
    url='https://github.com/bosha/pypushalot',
    keywords=['pushalot', 'push', 'api', 'windowsphone', 'wp'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
    test_suite='tests',
    tests_require=['coverage', 'httpretty']
)
