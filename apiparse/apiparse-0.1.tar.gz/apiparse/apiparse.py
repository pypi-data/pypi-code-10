'''
apiparse.py

Parse the patterns of apis of each module

Purpose
=======
    This program is used to list all the basic building block apis in
sources or files to understand the fundamental complexity of the program
development. The basic devleoquestion to be answered:
     - How may threads? types of threads/processes?
     - How much memory? Greedy and non-greedy memory allocation?
     - Atomic Locks and thread synchronization?
     - System APIs used?


Usage: usage : apiparse.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a, --showall         Show all apis
  -g APIGROUP, --group=APIGROUP
                        api groups:
  -p, --showpath        list file xtension paths
  -f FILENAME, --file=FILENAME
                        filename
  -d DESTNDIR, --destn=DESTNDIR
                        Destination Directory
  -t, --tree            Show Directory Tree


'''
import re
import pdb
import collections
import os
'''

memory_apis=
    memory access
    virtual memory
    memory mapping
    logical memory
    page allocator
    physical memory

processing_apis =
    processes
    threads
    synchronization
    scheduler
    interrupt context
    cpu specific

APIS=

functions = 
    system
    processing
    memory
    storage
    networking
    human interface

layers =
    user space
    virtual
    bridges
    functional
    device control
    hardware interface

'''

'''
apigroup -> apitype -> (api, filename, dirname)
apitype -> apis 

dirtree = {
            'dir1' : [file1, file2, file3, ..],
            'dir2' : [file4, file5, file6, ..],
        }

# function nodes
funcnodes = {
    funcname : {
        callee : {
            (funcstr, filename, dirname)
        }
        caller : {
            (funcstr, filename, dirname)
        }
    }
}

# API Categories
unixapis = {
    "memory" : {
        "malloc" : "Memory Allocation",
        "calloc" : "Allocate and initialize memory",
    }
    "scheduler" : {
        "fork" : "Fork Child Process",
        "pthread : "Spawn thread",
    }
}

linuxkernelapis = {
    "memory" : {

    }

    "scheduler" : {

    }
}

'''

CFileXtens = {
    #######
    # C/C++, Makefiles
    ##########
    "c"             :  { 'desc' : "C Source"},
    "h"             :  { 'desc' : "Header"},
    "cc"            :  { 'desc' : "Gnu C++ Source"},
    "cp"            :  { 'desc' : "Win C++ Source"},
    "cpp"           :  { 'desc' : "Win C++ Source"},
    "cxx"           :  { 'desc' : "Cxx C++ Source"},
    "include"       :  { 'desc' : "includes"},
    "inc"           :  { 'desc' : "inc Includes"},
}


CKeyWords = {
    #######
    # C/C++ Keywords
    #######
    "if"        : "conditional if",
    "else"      : "conditional else",
    "for"       : "for loop",
    "while"     : "while loop",
    "switch"    : "switch loop",
    "return"    : "return statements"
}

"""
cpattern
   (\w+)        # Match on api
   (\([\w\n\r\t\s,<>\\\[\]\"\-.=&':/*]*\)[\s\t\n\r]*)
                # signature between ( )
   ([{]|[;]|.*?\*\/|.*?\/\/)   # ending with ';' or '}'
"""
#cpattern = r"(\w+)([\s\t\n\r]*\(.*?\)[\s\t\n\r]*)([{]|[;]|.*?\*\/|.*?\/\/)"
cpattern = r"(\w+)[\s\t\n\r]*(\([\w\n\r\t\s,<>|\\\[\]\"\-.=&':/*\(\)]*\)[\s\t\n\r]*)([{]|[;]|.*?\*\/|.*?\/\/)"

"""
subpattern
   (\w+)       # Match on api
   (\([\w\n\r\t\s,<>\\\[\]\"\-.=&':/*]*\)[\s\t\n\r]*)
                # signature between ( )
   ((?![*][/])|[,]|[{]|[;])  # ending with ';' or '}'
"""
#subpattern = r"(\w+)([\t\s\n\r]*[(].*?[)][\t\s\n\r]*)($|(?![*][/])|[,]|[{]|[;])"
subpattern = r"(\w+)[\s\t\n\r]*(\([\w\n\r\t\s,<>|\\\[\]\"\-.=&':/*\(\)]*\)[\s\t\n\r]*)($|(?![*][/])|[,]|[{]|[;])"

class funcnode:
    _names = ['apiparse.globalapis']

    def __init__(self):
        self.funcnodes = collections.OrderedDict()
        self._GlobalApiList = collections.OrderedDict()
        self.filenode = ""
        self.dirnode = ""
        self.dirtree = collections.OrderedDict()
        self.showall = False
        self.everything = False
        self.apigroup = ""
        self.destndir = os.path.abspath(os.curdir)
        self.filename = ""
        self.showpath = False
        self.showdirtree = False
        self.getGlobalApiLists()
        self.parseCmdLineOptions()

    def __del__(self):
        pass

    def __call__(self, *args, **kwargs):
        #get all extn Nodes
        self.getGlobalApiLists()
        self.parseCmdLineOptions()

    def getGlobalApiLists(self):
        """
        Import the File extensions and store in a member dict variable.    
        """
        for name in self._names:
            try:
                mod = __import__(name, fromlist=['open'])
            except ImportError:
                raise ImportError("import %s error" % name)
        self._GlobalApiList = mod.globalapis_dict


    def addfunc(self, funcname, signature, callee):
        '''
        Add the funcname, signature and calling
        funcname : {
            "callee" : [
                (funcstr, filename, dirname)
            ]
            "caller" : [
                (funcstr, filename, dirname)
            ]
        ''' 
        if funcname not in self.funcnodes.keys():
            self.funcnodes[funcname] = collections.OrderedDict()
            self.funcnodes[funcname]["callee"] = list()
            self.funcnodes[funcname]["caller"] = list()
        fnode = self.funcnodes[funcname]
        ftuple = (funcname+signature, self.filenode, self.dirnode)
        ftype = 'callee'
        if callee is False: ftype = 'caller'
        if ftuple not in fnode[ftype]:
            fnode[ftype].append(ftuple)

    def showfilefunc(self, fname, cspace):
        for funcname in self.funcnodes.keys():
            if self.apigroup:
                subgroup = self.getapisubgroup(self.apigroup, funcname)
                if not subgroup:
                    continue
            fnode = self.funcnodes[funcname]
            for func, filename, dirname in fnode['caller']:
                if fname == filename:
                    print("    ",' '*5*cspace,"[=>]%s " %(func))
            for func, filename, dirname in fnode['callee']:
                if fname == filename:
                    print("    ",' '*5*cspace,"[++]%s " %(func))
                     
    def showfunc(self, funcname):
        fnode = self.funcnodes[funcname]
        if self.apigroup:
            subgroup = self.getapisubgroup(self.apigroup, funcname)
            if not subgroup:
                return

        print("\n %s:" %funcname)

        for func, filename, dirname in fnode['caller']:
            #print(dirname, filename)
            print("  [=>]",func)

        for func, filename, dirname in fnode['callee']:
            #print(dirname, filename)
            print("  (++)",func)

    def showapis(self):

        if self.filename:
            self.apiadd(self.filename)
        else:
            self.apiparse(self.destndir)

        print("="*50); print("*"*10,"LIST OF APIS","*"*10); print("="*50)
        if self.showdirtree is True:
            self.showtreedir()
            return

        for funcname in self.funcnodes.keys():
            self.showfunc(funcname)

    def showtreedir(self):
        if self.showdirtree is False:
            return

        for direntry in self.dirtree.keys():
            spaces = direntry.count(os.sep)
            print("\n",' '*4*spaces, " %s/" %(os.path.basename(direntry)))
            fdir  = self.dirtree[direntry]
            for fname in fdir:
                print(" ",' '*4*spaces,"-%s " %(fname))
                self.showfilefunc(fname, spaces)
                
    def apiparse(self, dirnode):
        for parent, dirs, files in os.walk(dirnode): 
            self.dirnode = parent
            if parent not in self.dirtree.keys():
                self.dirtree[parent] = list()
            for fname in files:
                filename = os.path.join(parent, fname)
                if os.path.isfile(filename):
                    index=[it.start() for it in re.finditer('[.]',filename)]
                    extn = filename[index[-1] + 1:]
                    if extn in CFileXtens.keys():
                        self.filenode = filename
                        self.dirtree[parent].append(filename)
                        self.apiadd(filename)
                  
    def apinode(self, fnstr):
        fn = fnstr[0].strip(' \t\n\r')
        signature = fnstr[1].strip(' \t\n\r')

        # Ignore functions within comments
        if (len(fnstr[2]) > 1): return
        callee = False
        if (fnstr[2].strip(' \t\n\r')  == ';'): callee = True

        #print("SIGN:",signature)
        if fn not in CKeyWords.keys():
            self.addfunc(fn, signature, callee)
        
        fsubexpr = re.compile(subpattern, re.I)
        fsubstr = fsubexpr.findall(signature)
        for subfunc in fsubstr:
            self.apinode(subfunc)
                
    def apiadd(self, src):
        #print(""*4,"-",src)

        with open(src) as fd:
            bufstr = fd.read()
            fexpr = re.compile(cpattern, re.I)
            fstr = fexpr.findall(bufstr)
            
            for func in fstr:
                #print(func)
                self.apinode(func)

    def getapisubgroup(self, group, funcname):
        apisubgroup = ""
        globapi = self._GlobalApiList;
        if group in globapi.keys():
            subgrpapi = globapi[group]
            for sgrp in subgrpapi.keys():
                apilist = subgrpapi[sgrp]
                if funcname in apilist.keys():
                    apisubgroup = sgrp
        return apisubgroup


    def showapigroups(self):
         globapi = self._GlobalApiList;
         for subgroup in globapi.keys():
            print("API GROUP:", subgroup)
            subgrpapi = globapi[subgroup]
            for sgrp in subgrpapi.keys():
                print("    (+)", sgrp)
                apilist = subgrpapi[sgrp]
                for api in apilist.keys():
                    print("        (-) %-20s : %s" %(api,apilist[api]))

    def parseCmdLineOptions(self):
        level = 0

        apigroups = ",".join([key for key in self._GlobalApiList.keys()])

        from optparse import OptionParser
        usage = "usage : %prog [options]"
        version = "%prog 1.0"
        parser = OptionParser(usage=usage, version=version)

        parser.add_option("-a", "--showall", action="store_true",
                            dest="showall", default=False,
                            help="Show all apis")
        parser.add_option("-e", "--everything", action="store_true",
                            dest="everything", default=False,
                            help="Every statement including if, for, while")
        parser.add_option("-g", "--group", action="store", type="string",
                            dest="apigroup", help="api groups:"+apigroups)
        parser.add_option("-s", "--showgroup", action="store_true", 
                            dest="showgroup", help="show api lists")
        parser.add_option("-p", "--showpath", action="store_true",
                            dest="showpath", default=False,
                            help="list file xtension paths")
        parser.add_option("-f", "--file", action="store", type="string",
                            dest="filename", help="filename")
        parser.add_option("-d", "--destn", action="store", type="string",
                            dest="destndir",default=os.curdir,
                            help="Destination Directory")
        parser.add_option("-t", "--tree", action="store_true",
                            dest="showdirtree",default=False,
                            help="Show Directory Tree")
        (options, args) = parser.parse_args()

        #print (options)

        if options.apigroup and options.apigroup not in [key for key in self._GlobalApiList.keys()]:
            print("Supported extn group are: %s" %apigroups)
            self.showapigroups()
            sys.exit()
        else:
            self.apigroup = options.apigroup

        if options.showgroup is True:
            self.showapigroups()
            sys.exit()
            
        if options.showall is True:
            self.showall = True
        if options.everything is True:
            self.everything = True

        if (options.destndir):
            self.destndir = options.destndir
        if (options.filename):
            self.filename = options.filename

        if (options.showdirtree is True):
            self.showdirtree = True
        if (options.showpath is True):
            self.showpath = True


    
