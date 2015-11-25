from setuptools import setup

setup(
    name='divdate',
    version='0.2',
    description='Division based date/time building',
    long_description='divdate is a Python module to build date and datetime object using the division operator.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    keywords='date time datetime division operator',
    url='http://github.com/soxofaan/divdate',
    author='Stefaan Lippens',
    author_email='soxofaan@gmail.com',
    license='MIT',
    packages=['divdate'],
    zip_safe=True,
    test_suite='nose.collector',
    tests_require=['nose'],
)
