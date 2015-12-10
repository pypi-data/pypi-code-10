#!/bin/python
# HAY QUE PENSAR BIEN ESTA CLASE: hay que ver el comportamiento esperado de todo esto...
# por ejemplo, el modo "exclusivo" que consistiria en q cuando se pone un fichero en la creacion, que se pone solo como search folder el directorio en que se ha encontrado.
# en otro caso, se ponen todos los directorios que se pasan como parametros
#
# Lo mismo para el "autoinclude", que cuando se encuentre el primero con el nombre del directorio entre los search folders, solo se ponga ese <- esto no lo tengo tan claro... habria que ver casos de uso
#
# Cuando se pone un fichero, ?se arrastra lo del exclusive?



import os
import logging
import glob
import ConfigParser

_LOGGER = logging.getLogger("[CONFIG]")

class Config():
    def __init__(self, filename, folders, exclusive_mode = False):
        self._search_folders = []
        self._config_filenames = []
        self._exclusive_mode = exclusive_mode
        # self.add_search_folders(folders)
        self.add_filename(filename, folders, onlyfirst)
    
    def add_filename(self, filename, folders = None, onlyfirst = False):
        possible_files = []
        if folders is None:
            folders = [""]

        filenames = self._possible_file_location(filename, self.folder_tree(folders))
        
        count = 0
        for f in filenames:
            if f not in self._config_filenames:
                _LOGGER.debug("adding file %s" % f)
                self._config_filenames.append(f)
                count += 1
                if (onlyfirst) and (count >= 1):
                    break
        return count

    def _possible_file_location(self, filename, folders):
        possible_filenames = []

        for folder in folders:
            folder = os.path.expanduser(folder).rstrip("/")
            wildcard_name = "%s/%s" % (folder, filename)
            files = glob.glob(wildcard_name)
            
            for f in files:
                possible_filenames.append(f)

        return possible_filenames

    def folder_tree(self, folders):
        folder_tree = []
        for folder in folders:
            folder = os.path.expanduser(folder).rstrip("/")
            if folder.startswith('/'):
                if os.path.isdir(folder) and (folder not in folder_tree):
                    folder_tree.append(folder)
            else:
                # It is relative, so we are trying to find any folder
                for s_folder in self._search_folders:
                    possible_folder = os.path.expanduser("%s/%s" % (s_folder, folder))
                    if os.path.isdir(possible_folder) and (possible_folder not in folder_tree):
                        folder_tree.append(possible_folder.rstrip("/"))
        return folder_tree
    
    def add_search_folders(self, folders):
        possible_folder = self.folder_tree(folders)
        count = 0
        for folder in possible_folder:
            if os.path.isdir(folder) and (folder not in self._search_folders):
                _LOGGER.info("adding %s as a search folder" % folder)
                self._search_folders.append(folder)
                count += 1
        return count
    
    def find_filename(self, filename):
        """
        This method is used to find a file (e.g. a file that contains the name of hosts) in the configuration folders
        """
        if filename.startswith('/'):
            _LOGGER.info("using absolute path for filename \"%s\"" % filename)
            return filename
    
        possible_locations = self._possible_file_location(filename, self._search_folders)
        if len(possible_locations) > 0:
            _LOGGER.info("found file %s" % possible_locations[0])
            return possible_locations[0]
    
        _LOGGER.info("file not found in config folders; so using path \"%s\" for filename \"%s\"" % (filename, filename))
        return filename
    
    def read(self, section, variables):
        config = ConfigParser.ConfigParser()
        config.read(self._config_filenames)
        
        options = {}
        if section in config.sections():
            options = config.options(section)
    
        for varname, value in variables.items():
            orig_varname = varname
            varname = varname.lower()
            if varname in options:
                try:
                    if isinstance(value, bool):
                        value = config.getboolean(section, varname)
                    elif isinstance(value, int):
                        value = config.getint(section, varname)
                    else:
                        value = config.get(section, varname)
                        if len(value) > 0:
                            value = value.split("#")[0].strip()
                except:
                    raise Exception("Invalid value for variable %s in config file" % orig_varname)
                    
            varname = varname.upper()
            self.__dict__[varname] = value
            _LOGGER.debug("%s=%s" % (varname, str(value)))

    def autoinclude(self, filename, section, varname):
        self.read(section, { varname: None })
        print self.DIRS
        while (self.add_search_folders([self.__dict__[varname]]) > 0) and (self.add_filename(filename) > 0):
            self.read(section, { varname: None })
    
if __name__ == '__main__':
    logging.basicConfig(filename=None, level=logging.DEBUG, format='%(asctime)-15s %(message)s')
    c = Config("f1.cfg", [ '/tmp/tests/' ])
    c.add_search_folders(["/tmp/tests"])
    c.add_search_folders(["conf.d"])
    # c.add_filename("*.cfg")
    # c.autoinclude("*.cfg", "s1", "DIRS")
    # c.add_filename("clues2.cfg")
    # c.add_search_folders(["plugins.d"])
    # c.add_filename("plugins.d/*.cfg")
    # c.find_filename("clues2.cfg")
    c.read("s1", {
        'V1': 0,
        'V2': 0,
        'V3': 0,
    })
    #c.find_filename("ipmi.hosts")
    #c.find_filename("ipmi.hostsss")
    #c.read({})
