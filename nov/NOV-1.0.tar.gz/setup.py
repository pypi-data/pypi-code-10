from distutils.core import setup, Extension

setup(name = "NOV", 
	version="1.0", 
	description="a testing project", 
	url="www.index.html", 
	author="Jonathan swift",
	author_email="jonathan_swift@gmail.com", 
	license="IPVL", 
	long_description="I am testing distutils warnings.",  
	platforms="Centos, Linux, Windows", # a list of strings or a comma-separated string
	packages = ["foo_dir", "foo_dir_2"], 
	py_modules=["subtract"], 
	package_data={'':['data/*.dat', 'data2/*.dat']}, 
	data_files=[('config', ['config/one.cfg', 'config/two.cfg', 'config/three.cfg'])],
	scripts = ['hello', 'script_folder/hello_first']  )





