import os

if os.name != "nt": 
   raise SystemError("This is not a windows nt system")


import sys
_ver_info = sys.version_info

pythonRegRoot = r"Software\Python\PythonCore\%s.%s" % (_ver_info[0], _ver_info[1])


from .NTRegReader import reader
pythonInstallationPath = reader.readValue( pythonRegRoot + '\InstallPath', "" )


