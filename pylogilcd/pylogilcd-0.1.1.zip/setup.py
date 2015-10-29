from distutils.core import setup, Extension
 
# define package info
package_name = 'pylogilcd' 
 
# define the name of the extension to use
extension_name    = '_pylogilcd'
extension_version = '0.1.1'

module = Extension( 
	extension_name,
	sources = ['pylogilcd.i', 'logilcd.cpp', 'surface.cpp', 'graphics.cpp'],
	swig_opts=['-c++'],
	include_dirs = ['.'],
	library_dirs = ['.'],
	libraries = ['LogitechLcd'],
	extra_compile_args = ['-std=c++11', '-D_hypot=hypot', '-D__NO_INLINE__'],
	extra_link_args = ['-mwindows']
	)
 
# create the extension and add it to the python distribution
setup( 
	name=package_name, 
	version=extension_version, 
	ext_modules=[
		module
		],
	package_data = {
		'.': ['LogitechLcd.dll']
	},
	py_modules = [
		'pylogilcd'
	]
)