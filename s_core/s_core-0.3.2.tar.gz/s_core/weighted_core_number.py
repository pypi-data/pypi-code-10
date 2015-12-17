"""
Find the weighted k-cores of a graph, also call s-core.

The s-core is found by recursively pruning nodes with strenght less than s.

See the following reference for details:

http://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.062819

"""
__author__ = 'Moreno Bonaventura (morenobonaventura@gmail.com)'

#	Copyright (C) 2015 by
#	Moreno Bonaventura <morenobonaventura@gmail.com>
#	All rights reserved.
#	BSD license.
__all__ = ['weighted_core_number'] #,'k_core','k_shell','k_crust','k_corona']

import networkx as nx
from collections import defaultdict

def weighted_core_number(G,weight='weight'):
	"""Return the core number for each vertex.

	A k-core is a maximal subgraph that contains nodes of degree k or more.

	The core number of a node is the largest value k of a k-core containing
	that node.

	Parameters
	----------
	G : NetworkX graph
	A weighted graph or directed graph

	Returns
	-------
	weighted_core_number : dictionary
	A dictionary keyed by node to the core number.

	Raises
	------
	NetworkXError
		The k-core is not defined for graphs with self loops or parallel edges.

	Notes
	-----
	Not implemented for graphs with parallel edges or self loops.

	For directed graphs the node strenght is defined to be the
	in-strenght + out-strenght.

	References
	----------
	.. [1] http://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.062819
	
	"""
	if G.is_multigraph():
		raise nx.NetworkXError(
				'MultiGraph and MultiDiGraph types not supported.')

	if G.number_of_selfloops()>0:
		raise nx.NetworkXError(
				'Input graph has self loops; the core number is not defined.',
				'Consider using G.remove_edges_from(G.selfloop_edges()).')

	if G.is_directed():
		import itertools
		def neighbors(v):
			return itertools.chain.from_iterable([G.predecessors_iter(v),G.successors_iter(v)])
	else:
		neighbors=G.neighbors_iter

	#--------------
	nbrs = dict((v,set(neighbors(v))) for v in G)
	
	strenght = G.degree(weight=weight)
	nodes_in_strenght_class = defaultdict(set)
	for n,s in strenght.iteritems():
		nodes_in_strenght_class[s].add(n)
	thresholds = nodes_in_strenght_class.keys()
	thresholds.sort()
	
	max_strenght = max(thresholds)
	
	residual_strenght = strenght
	s_core = {}
	while thresholds:
		s = thresholds.pop(0)
		print s,max_strenght,'\r',
		queue = nodes_in_strenght_class[s]		
		#pruning the queue
		while queue:
			v = queue.pop()
			s_core[v] = s
			for u in nbrs[v]:
				#print '  remove',v,'from',u
				nbrs[u].remove(v)
				nodes_in_strenght_class[residual_strenght[u]].remove(u)					
				residual_strenght[u] -= G[u][v][weight]
				nodes_in_strenght_class[residual_strenght[u]].add(u)
				if residual_strenght[u] <= s:
					queue.add(u)
				else:	
					thresholds.append(residual_strenght[u])
				#print ' ',residual_strenght
		thresholds.sort()

	return s_core