"""
calltree.py

Purpose
=======
* What is the problem statement?
    * Model the problem.
        - Equation
* How this Project solves the problem?
     * Use cases
* What is the value add? differentiator?

The understanding of the codeflow in a larger source of codebase, requires to
list the caller and callee relationships for a given function. For linux and
unix developers, cscope has been the primary utitlity to search and browse
through the code.

This utility uses the generated cscope database to list and display the
callgraph, which is stored in a image format. 


Interface
=========
* Command Line
* Web/GUI
* API

calltree.py
    -d <CSCOPE_DB>
    -f <function>
    -c <caller>
    -l <callee>
    -o <imageformat: jpg/png>

Data Structure
===============
* Data Abstraction
* Data Association
* Data Struture



Algorithms
==========
* Arrange/Sort/Search
* Memory Allocate/layout
* Queues/Slice/Schedule

"""

import re
import pdb
import os
import sys
import io
import re
import collections
import subprocess
import shlex
import pdb

import pyparsing
import pydotplus as pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class calltree:
    
    def __init__(self, function=None):
        command = ''
        self.func = function
        self.caller_level = 1
        self.callee_level = 1
        self.showall = False
        self.everything = False
        self.sourcedb = os.getenv("SOURCEDB")
        self.oformat  = "png"
        self.odir = os.path.abspath(os.curdir)
        self.cluster = ''

        self.funcnodes = collections.OrderedDict()
        self.parseCmdLineOptions()
        self.getsourcedb()
        self.createCallTree(self.func, self.caller_level, self.callee_level)

    def __call__(self):        
        command = ''

    def __del__(self):
        pass

    def setsourcedb(self, dbpath):
        """
        Get source database path
        """
        if dbpath and os.path.exists(dbpath):
            self.sourcedb = dbpath
        else:
            sys.exit("Invalid sourcedb Path!!")

    def getsourcedb(self):
        """
        Get source database path
        """
        if not self.sourcedb:
            if os.path.exists("cscope.out"):
                self.sourcedb  = "cscope.out"
            else:
                syss.exit("Set SOURCEDB env variable or specify -f")

        print("Using sourcedb:", self.sourcedb)
        os.chdir(os.path.dirname(self.sourcedb))

    def showtree(self):
        for func in self.funcnodes.keys():
            print("\n(*)", func)
            fnode = self.funcnodes[func]
            funcdef = fnode["define"]
            for ftuple in funcdef:
                print(' '*8,"-- %s <%d:%s>" %(' '.join(ftuple[2]),int(ftuple[1]), ftuple[0]))

            funcdef = fnode["caller"]
            if len(funcdef.keys()) > 0:
                print("\n")
            for cfunc in funcdef.keys():
                flist = funcdef[cfunc]
                print(" "*4,"%s" %(cfunc))
                for ftuple in flist:
                    print(' '*8,"|>>   %s <%d:%s> " %(' '.join(ftuple[2]),int(ftuple[1]), ftuple[0]))

            funcdef = fnode["callee"]
            if len(funcdef.keys()) > 0:
                print("\n"," "*2,"[%s]" %(func))
                print(" "*4,"|")
            for cfunc in funcdef.keys():
                flist = funcdef[cfunc]
                print(" "*4,"|<<   %s " %(cfunc))
                for ftuple in flist:
                    print(' '*8,'|'+'-'*4,"%s <%d:%s>" %(' '.join(ftuple[2]), int(ftuple[1]), ftuple[0]))

    def showgraph(self):
        
        graph = pydot.Dot(graph_type='digraph', rankdir="LR", splines="true",
                        nodesep=0.10, ranksep="1.1 equally", labelloc="top",             
                        labeljust="centered", ratio="auto", packMode="array_u",
                        compound="true", overlap="prism", clusterrank="global",
                        model="circuit")
        graph.set_graph_defaults(graph_type='record')


        graph.set_node_defaults(
                fontname="Verdana", 
                fontsize="12", 
                fillcolor="grey91;0.1:white",
                style="filled",fontcolor="black",
                labelfontname="Verdana", 
                labelfontsize="12",
                gradientangle=270,
                shape='rectangle')

        graph.set_edge_defaults(
                dir="forward",
                rank="same",
                color="midnightblue",
                fontsize="12",
                style="solid",
                penwidth=1,
                fontname="Verdana")


        for func in self.funcnodes.keys():
            print("showgraph:", func)
            fnode = self.funcnodes[func]
       
            calltree = '' 
            if (self.func == func):
                calltree = pydot.Cluster(graph_name="cluster_calltree_%s" %(func),
                            rank="same" ,style="filled", fillcolor="bisque1", fontsize=14)
 
                funcdef = fnode["define"]
                funcstr = func
                #for ftuple in funcdef:
                #    ftuplestr = "%s" %(' '.join(ftuple[2]))
                #    funcstr = "\n".join([funcstr,ftuplestr])

                funcgraph = pydot.Node(func, label=funcstr,
                            shape="rect",fontsize=26,
                            fillcolor="green",style="filled",
                            fontcolor="brown")
                calltree.add_node(funcgraph)
                self.cluster=calltree
            else:
                calltree = pydot.Cluster(graph_name="cluster_calltree_%s" %(func),
                            rank="same" , fontsize=14, style="dashed")
 
            graph.add_subgraph(calltree)

            funcdef = fnode["caller"]
            for cfunc in funcdef.keys():
                calltree.add_edge(pydot.Edge(cfunc, func, shape="eclipse"))
                print(func, "<---", cfunc)

            funcdef = fnode["callee"]
            for cfunc in funcdef.keys():
                calltree.add_edge(pydot.Edge(func, cfunc))
                print(func, "->", cfunc)

        calltreeimage = (self.func+'.'+self.oformat)
        print("\n... Calltree graph stored at: %s\n\n" %(os.path.join(self.odir,calltreeimage)))
        if (self.oformat == "jpg"):
            graph.write_jpg(os.path.join(self.odir,calltreeimage))
        else:
            graph.write_png(os.path.join(self.odir,calltreeimage))

        # render pydot by calling dot, no file saved to disk
        png_str = graph.create_png(prog='dot')
        sio = io.BytesIO()
        sio.write(png_str)
        sio.seek(0)
        img = mpimg.imread(sio)

        # plot the image
        imgplot = plt.imshow(img, aspect='equal')
        plt.show(block=True)
 
    def addfunc(self, func):
        """
        funcdict = {
            function : {
                define : {
                    funcname : (file, line, definitions)
                }
                callee : {
                    calleename : (file, line, definitions)
                }
                caller : {
                    callername : (file, line, definitions)
                }
            }
        }        
        """
        if func not in self.funcnodes.keys():
            self.funcnodes[func] = collections.OrderedDict()
            self.funcnodes[func]["define"] = list()
            self.funcnodes[func]["callee"] = collections.OrderedDict()
            self.funcnodes[func]["caller"] = collections.OrderedDict()

    def adddefine(self, func, filename, line, fdefine):
        """

        """
        if func not in self.funcnodes.keys():
            self.addfunc(func)

        fnode = self.funcnodes[func]
        funcdef = fnode["define"]
        ftuple = (filename, line, fdefine)
        if ftuple not in funcdef:
            funcdef.append(ftuple)

    def addcallee(self, func, callee, filename, line, cdefine):
        """

        """
        if func not in self.funcnodes.keys():
            self.addfunc(func)
        #if callee not in self.funcnodes.keys():
        #    self.addfunc(callee)

        fnode = self.funcnodes[func]
        funcdef = fnode["callee"]
        if callee not in funcdef.keys():
            funcdef[callee] = list()
        ftuple = (filename, line, cdefine)
        if ftuple not in funcdef[callee]:
            funcdef[callee].append(ftuple)

    def addcaller(self, func, caller, filename, line, cdefine):
        """

        """
        if func not in self.funcnodes.keys():
            self.addfunc(func)
        #if caller not in self.funcnodes.keys():
        #    self.addfunc(caller)

        fnode = self.funcnodes[func]
        funcdef = fnode["caller"]
        if caller not in funcdef.keys():
            funcdef[caller] = list()
        ftuple = (filename, line, cdefine)
        if ftuple not in funcdef[caller]:
            funcdef[caller].append(ftuple)

    def fsym(self, fname):
        self.run_cscope(0, fname)

    def fdefines(self, fname):
        output = self.run_cscope(1, fname)
        for outstr in output:
            if not outstr:
                continue
            cstr = outstr.split(' ')
            if len(cstr) > 2:
                self.adddefine(cstr[1], cstr[0], cstr[2], cstr[3:] )
            else:
                print(outstr)
                print("ERROR: output doesn't have func defines")

    def fcallees(self, fname, level):
        if (level > 0):
            output = self.run_cscope(2, fname)
            for outstr in output:
                if not outstr:
                    continue
                cstr = outstr.split(' ')
                if len(cstr) > 2:
                    self.addcallee(fname, cstr[1], cstr[0], cstr[2], cstr[3:] )
                else:
                    print(outstr)
                    print("ERROR: output doesn't have func callees")

    def fcaller(self, fname, level):
        if (level > 0):
            output = self.run_cscope(3, fname)
            for outstr in output:
                if not outstr:
                    continue
                cstr = outstr.split(' ')
                if len(cstr) > 2:
                    self.addcaller(fname, cstr[1], cstr[0], cstr[2], cstr[3:] )
                else:
                    print(outstr)
                    print("ERROR: output doesn't have func caller")


    def createCallTree(self,function, caller_level, callee_level):

        #print(function, caller_level, callee_level)
        if (caller_level <= 0) and (callee_level <= 0 ):
            return

        if function not in self.funcnodes.keys():
            print("processing %s" %(function))
            self.fdefines(function)
            self.fcaller(function, caller_level)
            self.fcallees(function, callee_level)

            if function in self.funcnodes.keys():
                fnode = self.funcnodes[function]
                funcdef = fnode["caller"]
                #print("CALLER:", caller_level, funcdef)
                if (len(funcdef.keys()) > 0) and (caller_level > 0):
                    # Unfold caller levels
                    if (self.showall is True):
                        caller_level = 1
                    else:
                        caller_level -= 1
                    allcallees = 0
                    if (self.everything is True):
                        allcallees = 1
                    for cfunc in funcdef.keys():
                        self.createCallTree(cfunc, caller_level, allcallees)

                funcdef = fnode["callee"]
                if (len(funcdef.keys()) > 0) and (callee_level > 0):
                    # Unfold callee levels
                    if (self.showall is True):
                        callee_level = 1
                    else:
                        callee_level -= 1
                    allcallers = 0
                    if (self.everything is True):
                        allcallers = 1
                    for cfunc in funcdef.keys():
                        self.createCallTree(cfunc, allcallers, callee_level)

    def fgrep(self, fstring):
        self.run_cscope(6, fname)

    def run_cscope(self, level, fname):
        # Construct the command to cscope
        cscope = '/usr/bin/cscope'

        command = "%s -f %s -L%d %s" %(cscope, self.sourcedb, level, fname)
        cmdstr = shlex.split(command)
        #print(cmdstr)

        outbyte = subprocess.Popen(cmdstr, stdout=subprocess.PIPE,universal_newlines=True)
        outbytestr=outbyte.communicate()[0]
        outstr=''.join(bytestr for bytestr in outbytestr)
        output=outstr.split('\n')

        #print(output)
        return output 

    def parseCmdLineOptions(self):
        """
            -d <CSCOPE_DB>
            -f <output format - jpg/png>
            -o <output dir>
            -l <show level of callers/callees>
            -a <all callers/callees>
            -c <callers>
            -e <callees>
        """
        level = 0

        from optparse import OptionParser
        usage = "usage : %prog [options] functionname"
        version = "%prog 1.0"
        parser = OptionParser(usage=usage, version=version)

        parser.add_option("--everything", action="store_true",
                            dest="everything", default=False,
                            help="Recursively show all callers and callees")
        parser.add_option("-a", "--showall", action="store_true",
                            dest="showall", default=False,
                            help="Show all callers and callees")
        parser.add_option("-c", "--callers", action="store_true",
                            dest="callers", default=False,
                            help="Recursively show all callers")
        parser.add_option("-e", "--callees", action="store_true",
                            dest="callees", default=False,
                            help="Recursively show all callees")
        parser.add_option("-l", "--level", action="store", type="int",
                            dest="level", default=1,
                            help="Show Level of callers/callees")
        parser.add_option("-f", "--format", action="store", type="string",
                            dest="outputformat", default="png",
                            help="output format jpg/png")
        parser.add_option("-o", "--outputdir", action="store", type="string",
                            dest="outputdir",default=os.path.abspath(os.curdir),
                            help="Storage directory for output files")
        parser.add_option("-d", "--db", action="store", type="string",
                            dest="sourcedb",default=os.getenv("SOURCEDB"),
                            help="cscope database (cscope.out)")
        (options, args) = parser.parse_args()
        #print(options)
        #print(args)

        if options.showall is True:
            self.showall = True
        if options.everything is True:
            self.everything = True

        self.setsourcedb(options.sourcedb)
        self.oformat = options.outputformat
        self.odir    = options.outputdir

        if (options.callers is True):
            self.caller_level = options.level

        if (options.callees is True):
            self.callee_level = options.level

        if (self.func == None and len(args) == 1):
            self.func = args[0]
        else:
            print(usage)
            sys.exit()
