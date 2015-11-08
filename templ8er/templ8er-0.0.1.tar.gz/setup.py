import os
from setuptools import setup, find_packages

version = '0.0.1'
description = "Templ8er - Simple Template Generator"

script_dir = os.path.dirname(os.path.realpath(__file__))

try:
    import pypandoc
    long_description = lambda f: pypandoc.convert(f, 'rst', format='md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = lambda f: open(f, 'r').read()
except:
    long_description = description

modules = [f for f in os.listdir(os.path.join(script_dir, 'main/src/modules')) if os.path.isfile(f)]

setup(
    name = "templ8er",
    version = version,
    url = 'https://github.com/AkihikoITOH/templ8er',
    license = 'MIT',
    description = description,
    long_description = long_description('./README.md'),
    author = 'ITOH Akihiko',
    packages = find_packages('main'),
    package_dir = {'': 'main'},
    scripts = modules,
    # scripts = ['main/modules/', 'main/templates/'],
    package_data={ 'src': ['*.py']},
    install_requires = ['setuptools', 'pypandoc', 'click', 'PyYaml', 'Jinja2'],
    entry_points="""
    [console_scripts]
    t8er = src.templ8er:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        # 'Topic :: Software Development :: Bug Tracking',
    ],
    # test_suite = 'nose.collector',
)
