# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 12:34:26 2015

@author: Wiwat Owasirikul
"""

from distutils.core import setup 


packagedata={'pypcm': ['PCM_data/*','QSAR_data/*']}


setup(name = 'pypcm', 

	version = '1.0', 
	
	description ="Workflow for QSAR/QPSAR and Proteochemometric modeling",
	
	author = "Wiwat Owasirikul",
	
	author_email = "wiwat.owa@mahidol.ac.th",
	
	url ="https://github.com/cdmbi/PCM",
	
	license = "GPL",
	
	packages = ['pypcm'],

      install_requires=['pydpi'],
	
	package_data=packagedata,
	
#	data_files = datafiles,
	
	package_dir={'pypcm':'src/pypcm'},
	
	scripts = [],
	
	py_modules = []

	)