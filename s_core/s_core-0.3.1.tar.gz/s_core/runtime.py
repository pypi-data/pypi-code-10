import networkx as nx
from weighted_core_number import weighted_core_number

G = nx.read_weighted_edgelist('test_net.txt')

#TODO provare un erdos reny con pesi random


#print G.edges(data=True)
print ' stren:\n',G.degree(weight='weight')
print ''

s_core =  weighted_core_number(G)
print '\n weighted:'
print s_core

print '\n unweighted:'
print nx.core_number(G)