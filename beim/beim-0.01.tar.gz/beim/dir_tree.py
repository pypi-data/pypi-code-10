#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                Jiao Lin
#                        California Institute of Technology
#                        (C) 2006  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 



class Node:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.children = []
        self.path = None
        return


    def addChild(self, child):
        self.children.append( child )
        return


    def search( self, description ):
        "search a node with given description and return path"
        if self.description == description: return self
        for child in self.children:
            candidate = child.search( description )
            if candidate: return candidate
            continue
        return

    pass # end of Node



class SetPaths:

    def render(self, node, root = ''):
        self._stack = list(os.path.split( root )[:-1])
        self.onNode( node )
        return


    def onNode(self, node):
        self._stack.append( node.name )
        node.path = os.path.join(*self._stack)
        for child in node.children:
            self.onNode( child )
            continue
        self._stack.pop()
        return

    pass # end of SetPaths


_setPaths = SetPaths()

def setPaths( node, root ):
    """set path of each node. The root node's path is set to the
    path given by parameter 'root'"""
    _setPaths.render( node, root )
    return


# ------------------------------------------------------------
# printing facility
class Printer:

    indentation = '  '
    expansion_sign = '+'

    def render(self, node):
        self._indentLevel = 0
        self.onNode( node )
        return


    def onNode(self, node):
        self._write( "%s: %s" % (node.path, node.description))
        self.indent()
        for child in node.children:
            self.onNode( child )
            continue
        self.outdent()
        return

    def indent(self): self._indentLevel += 1
    def outdent(self): self._indentLevel -= 1
    def _write(self,s):
        print(("%s%s%s" % (
            self.indentation * self._indentLevel,
            self.expansion_sign, s )))

    pass # end of Printer


_printer = Printer()

def printTree( node ):
    _printer.render( node )
    return



def createTree( d ):
    name,description, children = d
    n = Node( name, description )
    for child in children:
        childNode = createTree( child )
        n.addChild( childNode )
        continue
    return n


import os



# version
__id__ = "$Id: __init__.py 400 2006-04-15 23:41:16Z jiao $"

#  End of file 
