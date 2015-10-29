#!/usr/bin/python
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

from lutin import debug
from lutin import system
from lutin import tools
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.help="SDK: Android SDK basic interface java\n"
		# jar file:
		jar_file_path=os.path.join(target.path_sdk, "platforms", "android-" + str(target.board_id), "android.jar")
		# TODO : Check if the android sdk android.jar is present ...
		self.valid = True
		# todo : create a searcher of the presence of the library:
		self.add_export_SRC(jar_file_path)
		self.add_export_flag_LD("-ldl")
		self.add_export_flag_LD("-llog")
		self.add_export_flag_LD("-landroid")


