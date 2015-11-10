from setuptools import setup, find_packages
from os import path

# pandoc and pypandoc are required for building reStructureText documentation for PyPi
try:
	from pypandoc import convert
	read_md_and_convert_to_rst = lambda file: convert(file, 'rst')
except ImportError:
	print("warning: pypandoc module not found, could not convert Markdown to RST")
	read_md_and_convert_to_rst = lambda file: open(file, 'r').read()

script_location = path.abspath(path.dirname(__file__))
readme_path = path.join(script_location, 'README.md')

long_description = read_md_and_convert_to_rst(readme_path)

setup(
	name="practichem_biodetector",
	version="1.0",
	description="Biodetector control class",
	long_description=long_description,
	author="Practichem",
	author_email="opensource@practichem.com",
	license="Apache License, Version 2.0",
	install_requires=['pyserial>=2.7', 'practichem_device>=1.0'],
	packages=find_packages(),
	zip_safe=True,
	url="https://www.practichem.com",
	classifiers=[
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	])
