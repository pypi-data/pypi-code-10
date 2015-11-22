from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name='statx',
    version='0.0.2',
    description='A tool to count things',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    packages=find_packages(exclude=['script']),
    install_requires=['six'],
    license='MIT',
    url='https://github.com/lorien/statx',
    keywords="stat statistics stats",
    author="Gregory Petukhov",
    author_email='lorien@lorien.name',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries'
    ],
)
