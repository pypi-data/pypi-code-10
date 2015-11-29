from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'charlesbot',
]

test_requirements = [
    'asynctest',
    'coverage',
    'flake8',
]

setup(
    name='charlesbot-pagerduty',
    version='1.0.1',
    description="A charlesbot pagerduty plugin",
    long_description=readme,
    author="Marvin Pinto",
    author_email='marvin@pinto.im',
    url='https://github.com/marvinpinto/charlesbot-pagerduty',
    packages=[
        'charlesbot_pagerduty',
    ],
    package_dir={'charlesbot_pagerduty':
                 'charlesbot_pagerduty'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='slack robot chatops charlesbot charlesbot-pagerduty',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
