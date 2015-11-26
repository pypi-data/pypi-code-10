# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Fred Boudon <fred.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
################################################################################
"""This module provide a set of concepts to add properties to graph elements.

TODO: stupid implementation that do not ensure that ids in properties are valid
graph elements.
"""

from graph import Graph, InvalidVertex, InvalidEdge


class InvalidProperty(Exception):
    """Exception used when a property is missing."""
    pass


class PropertyGraph(Graph):
    """Simple implementation of PropertyGraph using
    dict as properties and two dictionaries to
    maintain these properties
    """

    def __init__(self, graph=None, **kwds):
        self._vertex_property = {}
        self._edge_property = {}
        self._graph_property = {}
        Graph.__init__(self, graph, **kwds)

    def vertex_property_names(self):
        """Names of properties associated to vertices.

        return:
         - (iter of str)
        """
        return self._vertex_property.iterkeys()

    def vertex_properties(self):
        """Iterate on all properties associated to vertices.

        return:
         - (iter of dict of (vid, any))
        """
        return self._vertex_property.items()

    def vertex_property(self, property_name):
        """Return a map between vid and data for all vertices where
        property_name is defined

        args:
         - property_name (str): name identifier of the property
        return:
         - (dict of (vid, any))
        """
        try:
            return self._vertex_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on vertices"
                                  % property_name)

    def edge_property_names(self):
        """Names of properties associated to edges.

        return:
         - (iter of str)
        """
        return self._edge_property.iterkeys()

    def edge_properties(self):
        """Iterate on all properties associated to edges.

        return:
         - (iter of dict of (eid, any))
        """
        return self._edge_property.items()

    def edge_property(self, property_name):
        """Return a map between eid and data for all edges where
        property_name is defined

        args:
         - property_name (str): name identifier of the property
        return:
         - (dict of (eid, any))
        """
        try:
            return self._edge_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on edges"
                                  % property_name)

    def graph_property_names(self):
        """Names of properties associated to the graph.

        return:
         - (iter of str)
        """
        return self._graph_property.iterkeys()

    def graph_properties(self):
        """Iterate on all properties associated to the graph.

        return:
         - (iter of (str, any))
        """
        return self._graph_property.iteritems()

    def graph_property(self, property_name):
        """Return the value of a property associated to the graph.

        args:
         - property_name (str): name identifier of the property
        return:
         - (any)
        """
        try:
            return self._graph_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on graph"
                                  % property_name)

    ###########################################################
    #
    #        mutable property concept
    #
    ###########################################################
    def add_vertex_property(self, property_name, values=None):
        """Add a new map between vid and a data.

        args:
         - property_name (str): name identifier for this property
         - values (dict of (vid, any)): pre set values for some vertices.
                        If None (default), property will be emtpy.
        """
        if property_name in self._vertex_property:
            raise InvalidProperty("property %s is already defined on vertices"
                                  % property_name)
        if values is None:
            values = {}
        self._vertex_property[property_name] = values

    def remove_vertex_property(self, property_name):
        """Remove a given property.

        args:
         - property_name (str): name identifier for this property
        """
        try:
            del self._vertex_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on vertices"
                                  % property_name)

    def add_edge_property(self, property_name, values=None):
        """Add a new map between eid and a data.

        args:
         - property_name (str): name identifier for this property
         - values (dict of (eid, any)): pre set values for some edge.
                        If None (default), property will be emtpy.
        """
        if property_name in self._edge_property:
            raise InvalidProperty("property %s is already defined on edges"
                                  % property_name)
        if values is None:
            values = {}
        self._edge_property[property_name] = values

    def remove_edge_property(self, property_name):
        """Remove a given property.

        args:
         - property_name (str): name identifier for this property
        """
        try:
            del self._edge_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on edges"
                                  % property_name)

    def add_graph_property(self, property_name, value=None):
        """Add a new property to the graph.

        args:
         - property_name (str): name identifier for the property
         - value (any): value (defaut None) associated to this property
        """
        if property_name in self._graph_property:
            raise InvalidProperty("property %s is already defined on graph"
                                  % property_name)

        self._graph_property[property_name] = value

    def remove_graph_property(self, property_name):
        """Remove a given property.

        args:
         - property_name (str): name identifier for this property
        """
        try:
            del self._graph_property[property_name]
        except KeyError:
            raise InvalidProperty("property %s is undefined on graph"
                                  % property_name)

    ###########################################################
    #
    #        mutable property concept
    #
    ###########################################################
    def remove_vertex(self, vid):
        for prop in self._vertex_property.itervalues():
            prop.pop(vid, None)
        Graph.remove_vertex(self, vid)

    # remove_vertex.__doc__ = Graph.remove_vertex.__doc__

    def remove_edge(self, eid):
        for prop in self._edge_property.itervalues():
            prop.pop(eid, None)
        Graph.remove_edge(self, eid)

    # remove_edge.__doc__ = Graph.remove_edge.__doc__

    def clear(self):
        for prop in self._vertex_property.itervalues():
            prop.clear()
        for prop in self._edge_property.itervalues():
            prop.clear()
        self._graph_property.clear()
        Graph.clear(self)

    # clear.__doc__ = Graph.clear.__doc__

    def clear_edges(self):
        for prop in self._edge_property.itervalues():
            prop.clear()
        Graph.clear_edges(self)

    # clear_edges.__doc__ = Graph.clear_edges.__doc__

    def extend(self, graph):
        # add and translate the vertex and edge ids of the second graph
        trans_vid, trans_eid = Graph.extend(self, graph)

        if isinstance(graph, PropertyGraph):
            # update graph properties
            for name, prop in graph.vertex_properties():
                if name not in self.vertex_property_names():
                    self.add_vertex_property(name)

                self_prop = self.vertex_property(name)
                for vid, data in prop.items():
                    self_prop[trans_vid[vid]] = data

            # update edge properties
            for name, prop in graph.edge_properties():
                if name not in self.edge_property_names():
                    self.add_edge_property(name)

                self_prop = self.edge_property(name)
                for eid, data in prop.items():
                    self_prop[trans_eid[eid]] = data

            # update graph properties
            for name, data in graph.graph_properties():
                if name not in self.graph_properties():
                    self.add_graph_property(name, data)

        return trans_vid, trans_eid

        # extend.__doc__ = Graph.extend.__doc__
