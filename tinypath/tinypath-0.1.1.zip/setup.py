try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.rst").read(), 
	name="""tinypath""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	py_modules=['tinypath'],
	url="""http://github.com/karimbahgat/tinypath""",
	version="""0.1.1""",
	keywords="""paths files folders organizing""",
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop'],
	description="""Tinypath is a tiny object-oriented file path module that provides only the most crucial and commonly needed functionality, making it easy to learn and efficient to use.""",
	)
