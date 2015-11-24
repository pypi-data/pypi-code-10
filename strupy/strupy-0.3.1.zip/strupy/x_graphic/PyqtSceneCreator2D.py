'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2015-11-23
This file is part of Struthon.
Struthon is a range of free open source structural engineering design 
Python applications.
http://struthon.org/

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
File version 0.x changes:
- .....
'''

import sys

from PyQt4 import QtGui

import strupy.units as u
    
class PyqtSceneCreator2D():
    def __init__(self):
        self.scene = QtGui.QGraphicsScene()
        self.unit = 10 * u.mm
    
    def set_GraphicsViewObiect(self, somegraphicsView):
        self.graphicsView = somegraphicsView
    
    def set_unit(self, newunit=10*u.mm):
        self.unit = newunit
        
    def change_unit(self, value=2*u.mm):
        if not (self.unit + value) <= 0.1*u.mm:
            self.unit += value
    
    def diminpixels(self, dim):
        pixels = []
        for i in dim :
            pixels.append((i/self.unit).asNumber())
        return pixels 
    
    def addLine(self, p1, p2):
        p1=self.diminpixels(p1)
        p2=self.diminpixels(p2)
        self.scene.addLine(p1[0], -p1[1], p2[0], -p2[1])
        
    def addText(self, text, p):
        p=self.diminpixels(p)
        self.scene.addText(text).setPos(p[0], -p[1])
    
    def clearScene(self):
        self.scene.clear()

    def ShowOnGraphicsViewObiect(self):
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()

#----Test if main
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    grview = QtGui.QGraphicsView()
    #----
    ScienceScene = PyqtSceneCreator2D()
    ScienceScene.set_GraphicsViewObiect(grview)
    ScienceScene.ShowOnGraphicsViewObiect()
    #----
    p1 = [0*u.cm, 0*u.mm]
    p2 = [10*u.cm, 0*u.mm]
    ScienceScene.addLine(p1, p2)
    p3 = [4*u.cm, 4*u.mm]
    p4 = [-10*u.cm, -10*u.mm]
    ScienceScene.addLine(p3, p4)
    ScienceScene.addText('lala', p1)
    #----
    from strupy.steel.SectionBase import SectionBase
    base = SectionBase()
    for i in base.get_database_sectionlistwithtype('HHEA'):
        print i
        base.draw_sectiongeometry(ScienceScene, i)
    #---
    sys.exit(app.exec_())