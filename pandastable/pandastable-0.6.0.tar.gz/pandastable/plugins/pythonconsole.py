#!/usr/bin/env python
"""
    DataExplore plugin for adding a python console
    Created Oct 2015
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from pandastable.plugin import Plugin
import tkinter
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from threading import *
import code
import readline

class myConsole(code.InteractiveConsole):
    def __init__(self):
        return

class ConsoleThread(Thread):
    def __init__(self, table):
        Thread.__init__(self)
        self.table = table

    def run(self):

        #readline.parse_and_bind("tab: complete")
        table = self.table
        df = self.table.model.df
        vars = globals().copy()
        vars.update(locals())
        self.shell = code.InteractiveConsole(vars)
        self.shell.interact()
        return

class ConsolePlugin(Plugin):
    """Plugin for DataExplore"""

    capabilities = ['gui','uses_sidepane']
    requires = ['']
    menuentry = 'Python Console'
    gui_methods = {}
    version = '0.1'

    def main(self, parent):

        if parent==None:
            return
        self.parent = parent
        self._doFrame()
        table = self.table = self.parent.getCurrentTable()
        #df = self.table.model.df

        #stdout = sys.stdout
        sys.stdout = self
        sys.stderr = self

        self.consoleThread = ConsoleThread(table)
        self.mainwin.after(100, self.consoleThread.start)

        self.ttyText = Text(self.mainwin, wrap='word', width=50, height=8)
        self.ttyText.pack(side=LEFT,fill=BOTH,expand=1)

        bf = Frame(self.mainwin, padding=2)
        bf.pack(side=LEFT,fill=BOTH)
        b = Button(bf, text="Run", command=self.execute)
        b.pack(side=TOP,fill=X,expand=1)
        b = Button(bf, text="Close", command=self.quit)
        b.pack(side=TOP,fill=X,expand=1)
        b = Button(bf, text="About", command=self._aboutWindow)
        b.pack(side=TOP,fill=X,expand=1)
        return

    def write(self, string):
        self.ttyText.insert('end', string)
        self.ttyText.see('end')

    def errors(self, string):
        self.ttyText.insert('end', string)
        self.ttyText.see('end')

    def read(self,string):
        self.consoleThread.shell.runcode(string)
        return

    def execute(self):

        col = self.ttyText.index("end")
        cmd = self.ttyText.get("end-1c linestart", "end")
        cmd = cmd.strip('>>>').strip()

        c = self.consoleThread.shell.compile(cmd)
        self.consoleThread.shell.runcode(c)

        print (self.table.model.df)
        self.table.redraw()
        self.table.update_idletasks()
        return

    def _doFrame(self):
        """Create main frame"""

        if 'uses_sidepane' in self.capabilities:
            table = self.parent.getCurrentTable()
            self.mainwin = Frame(table.parentframe)
            self.mainwin.grid(row=5,column=0,columnspan=2,sticky='news')
            self.table = table

        self.mainwin.bind("<Destroy>", self.quit)
        self.ID=self.menuentry
        return

    def quit(self, evt=None):
        """Override this to handle pane closing"""

        self.mainwin.destroy()
        #self.consoleThread.stop()
        #sys.stdout = stdout
        return

    def about(self):
        """About this plugin"""

        txt = "This plugin implements ...\n"+\
               "version: %s" %self.version
        return txt
