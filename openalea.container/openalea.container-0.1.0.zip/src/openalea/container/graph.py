# -*- coding: utf-8 -*-
#
#       Graph : graph package
#
#       Copyright or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
#
"""This module provide a simple pure python implementation
for a graph interface

does not implement copy concept
"""

from id_dict import IdDict


class GraphError(Exception):
    """
    base class of all graph exceptions
    """


class InvalidEdge(GraphError, KeyError):
    """
    exception raised when a wrong edge id is provided
    """


class InvalidVertex(GraphError, KeyError):
    """
    exception raised when a wrong vertex id is provided
    """


class Graph(object):
    """Directed graph with multiple links
    in this implementation :

        - vertices are tuple of edge_in,edge_out
        - edges are tuple of source,target
    """

    def __init__(self, graph=None, idgenerator="set"):
        """constructor

        if graph is not none make a copy of the topological structure of graph
        (i.e. don't use the same id)

        args:
          - graph (Graph): the graph to copy, default=None
          - idgenerator (str): type of idgenerator to use, default 'set'
        """
        self._vertices = IdDict(idgenerator=idgenerator)
        self._edges = IdDict(idgenerator=idgenerator)
        if graph is not None:
            self.extend(graph)

    # ##########################################################
    #
    # Graph concept
    #
    # ##########################################################
    def source(self, eid):
        """Retrieve the source vertex of an edge

        args:
         - eid (int):  edge id

        return:
         - (int): vertex id
        """
        try:
            return self._edges[eid][0]
        except KeyError:
            raise InvalidEdge(eid)

    def target(self, eid):
        """Retrieve the target vertex of an edge

        args:
         - eid (int):  edge id

        return:
         - (int): vertex id
        """
        try:
            return self._edges[eid][1]
        except KeyError:
            raise InvalidEdge(eid)

    def edge_vertices(self, eid):
        """Retrieve both source and target vertex of an edge

        args:
         - eid (int):  edge id

        return:
         - (int, int): source id, target id
        """
        try:
            return self._edges[eid]
        except KeyError:
            raise InvalidEdge(eid)

    def edge(self, source, target):
        """Find the matching edge with same source and same target
        return None if it don't succeed

        args:
         - source (int): source vertex
         - target (int): target vertex

        return:
         - (int): edge id with same source and target
         - (None): if search is unsuccessful
        """
        if target not in self:
            raise InvalidVertex(target)

        for eid in self.out_edges(source):
            if self.target(eid) == target:
                return eid

        return None

    def __contains__(self, vid):
        """magic alias for `has_vertex`
        """
        return self.has_vertex(vid)

    def has_vertex(self, vid):
        """test whether a vertex belong to the graph

        args:
         - vid (int): id of vertex

        return:
         - (bool)
        """
        return vid in self._vertices

    def has_edge(self, eid):
        """test whether an edge belong to the graph

        args:
         - eid (int): id of edge

        return:
         - (bool)
        """
        return eid in self._edges

    def is_valid(self):
        """Test the validity of the graph

        return:
         - (bool)
        """
        return True

    # ##########################################################
    #
    # Vertex List Graph Concept
    #
    # ##########################################################
    def vertices(self):
        """Iterator on all vertices

        return:
         - (iter of int)
        """
        return iter(self._vertices)

    def __iter__(self):
        """Magic alias for `vertices`
        """
        return iter(self._vertices)

    def nb_vertices(self):
        """Total number of vertices in the graph

        return:
         - (int)
        """
        return len(self._vertices)

    def __len__(self):
        """Magic alias for `nb_vertices`
        """
        return self.nb_vertices()

    def in_neighbors(self, vid):
        """Iterator on the neighbors of vid
        where edges are directed from neighbor to vid

        args:
         - vid (int): vertex id

        return:
         - (iter of int): iter of vertex id
        """
        if vid not in self:
            raise InvalidVertex(vid)
        neighbors_list = [self.source(eid) for eid in self._vertices[vid][0]]
        return iter(set(neighbors_list))

    def out_neighbors(self, vid):
        """Iterator on the neighbors of vid
        where edges are directed from vid to neighbor

        args:
         - vid (int): vertex id

        return:
         - (iter of int): iter of vertex id
        """
        if vid not in self:
            raise InvalidVertex(vid)
        neighbors_list = [self.target(eid) for eid in self._vertices[vid][1]]
        return iter(set(neighbors_list))

    def neighbors(self, vid):
        """Iterator on all neighbors of vid both in and out

        args:
         - vid (int): vertex id

        return:
         - (iter of int): iter of vertex id
        """
        neighbors_list = list(self.in_neighbors(vid))
        neighbors_list.extend(self.out_neighbors(vid))
        return iter(set(neighbors_list))

    def nb_in_neighbors(self, vid):
        """Number of in neighbors of vid
        where edges are directed from neighbor to vid

        args:
         - vid (int): vertex id

        return:
         - (int)
        """
        neighbors_set = list(self.in_neighbors(vid))
        return len(neighbors_set)

    def nb_out_neighbors(self, vid):
        """Number of out neighbors of vid
        where edges are directed from vid to neighbor

        args:
         - vid (int): vertex id

        return:
         - (int)
        """
        neighbors_set = list(self.out_neighbors(vid))
        return len(neighbors_set)

    def nb_neighbors(self, vid):
        """Total number of both in and out neighbors of vid

        args:
         - vid (int): vertex id

        return:
         - (int)
        """
        neighbors_set = list(self.neighbors(vid))
        return len(neighbors_set)

    # ##########################################################
    #
    # Edge List Graph Concept
    #
    # ##########################################################
    def _iter_edges(self, vid):
        """
        internal function that perform 'edges' with vid not None
        """
        link_in, link_out = self._vertices[vid]
        for eid in link_in:
            yield eid
        for eid in link_out:
            yield eid

    def edges(self, vid=None):
        """Iterate on all edges connected to a given vertex.

        If vid is None (default), iterate on all edges in the graph

        args:
         - vid (int): vertex holdings edges, default (None)

        return:
         - (iter of int): iterator on edge ids
        """
        if vid is None:
            return iter(self._edges)
        if vid not in self:
            raise InvalidVertex(vid)
        return self._iter_edges(vid)

    def nb_edges(self, vid=None):
        """Number of edges connected to a given vertex.

        If vid is None (default), total number of edges in the graph

        args:
         - vid (int): vertex holdings edges, default (None)

        return:
         - (int)
        """
        if vid is None:
            return len(self._edges)
        if vid not in self:
            raise InvalidVertex(vid)
        return len(self._vertices[vid][0]) + len(self._vertices[vid][1])

    def in_edges(self, vid):
        """Iterate on all edges pointing to a given vertex.

        args:
         - vid (int): vertex target of edges

        return:
         - (iter of int): iterator on edge ids
        """
        print "in", vid, vid in self
        if vid not in self:
            raise InvalidVertex(vid)
        for eid in self._vertices[vid][0]:
            yield eid

    def out_edges(self, vid):
        """Iterate on all edges away from a given vertex.

        args:
         - vid (int): vertex source of edges

        return:
         - (iter of int): iterator on edge ids
        """
        if vid not in self:
            raise InvalidVertex(vid)
        for eid in self._vertices[vid][1]:
            yield eid

    def nb_in_edges(self, vid):
        """Number of edges pointing to a given vertex.

        args:
         - vid (int): vertex target of edges

        return:
         - (int)
        """
        if vid not in self:
            raise InvalidVertex(vid)
        return len(self._vertices[vid][0])

    def nb_out_edges(self, vid):
        """Number of edges away from a given vertex.

        args:
         - vid (int): vertex source of edges

        return:
         - (int)
        """
        if vid not in self:
            raise InvalidVertex(vid)
        return len(self._vertices[vid][1])

    # ##########################################################
    #
    # Mutable Vertex Graph concept
    #
    # ##########################################################
    def add_vertex(self, vid=None):
        """Add a vertex to the graph.

        If vid is not provided create a new vid

        args:
         - vid (int): id to use. If None (default) will generate a new one

        return:
         - vid (int): id used for the new vertex
        """
        try:
            return self._vertices.add((set(), set()), vid)
        except KeyError:
            raise InvalidVertex(vid)

    def remove_vertex(self, vid):
        """Remove a specified vertex of the graph.

        Also remove all edge attached to it.

        args:
         - vid (int): id of vertex to remove
        """
        if vid not in self:
            raise InvalidVertex(vid)
        link_in, link_out = self._vertices[vid]
        for edge in list(link_in):
            self.remove_edge(edge)
        for edge in list(link_out):
            self.remove_edge(edge)
        del self._vertices[vid]

    def clear(self):
        """Remove all vertices and edges
        don't change references to objects
        """
        self._edges.clear()
        self._vertices.clear()

    # ##########################################################
    #
    # Mutable Edge Graph concept
    #
    # ##########################################################
    def add_edge(self, sid, tid, eid=None):
        """Add an edge to the graph.

        If eid is not provided generate a new one.

        args:
         - sid (int): id of source vertex
         - tid (int): id of target vertex
         - eid (int): id to use. If None (default) will generate a new one

        return:
         - eid (int): id used for new edge
        """
        if sid not in self:
            raise InvalidVertex(sid)
        if tid not in self:
            raise InvalidVertex(tid)
        try:
            eid = self._edges.add((sid, tid), eid)
        except KeyError:
            raise InvalidEdge(eid)
        self._vertices[sid][1].add(eid)
        self._vertices[tid][0].add(eid)
        return eid

    def remove_edge(self, eid):
        """Remove a specified edge from the graph.

        args:
         - eid (int): id of edge to remove
        """
        if not self.has_edge(eid):
            raise InvalidEdge(eid)
        sid, tid = self._edges[eid]
        self._vertices[sid][1].remove(eid)
        self._vertices[tid][0].remove(eid)
        del self._edges[eid]

    def clear_edges(self):
        """Remove all the edges of the graph
        don't change references to objects
        """
        self._edges.clear()
        for vid, (in_set, out_set) in self._vertices.iteritems():
            in_set.clear()
            out_set.clear()

    # ##########################################################
    #
    # Extend Graph concept
    #
    # ##########################################################
    def extend(self, graph):
        """Add the specified graph to self, create new vid and eid

        args:
         - graph (Graph): the graph to add

        return:
         - (dict of (int, int)): mapping between vertex id in graph and
                                 vertex id in extended self
         - (dict of (int, int)): mapping between edge id in graph and
                                 edge id in extended self
        """
        # vertex adding
        trans_vid = {}
        for vid in list(graph.vertices()):
            trans_vid[vid] = self.add_vertex()

        # edge adding
        trans_eid = {}
        for eid in list(graph.edges()):
            sid = trans_vid[graph.source(eid)]
            tid = trans_vid[graph.target(eid)]
            trans_eid[eid] = self.add_edge(sid, tid)

        return trans_vid, trans_eid

    def sub_graph(self, vids):
        """
        """
        raise NotImplemented
        # from copy import deepcopy
        # vids = set(vids)
        #
        # result = deepcopy(self)
        # result._vertices.clear()
        # result._edges.clear()
        #
        # for key, edges in self._vertices.items():
        #     if key in vids:
        #         inedges, outedges = edges
        #         sortedinedges = set(
        #             [eid for eid in inedges if self.source(eid) in vids])
        #         sortedoutedges = set(
        #             [eid for eid in outedges if self.target(eid) in vids])
        #         result._vertices.add((sortedinedges, sortedoutedges), key)
        #         for eid in sortedoutedges:
        #             result._edges.add(self._edges[eid], eid)
        #
        # return result
