## @package graph_modification
# This module contains functions to edit graph contents:
# Adding nodes, edges, attributes...
import networkx as nx
import random as rd

## 
# assign type and opinion attributes to all nodes of the graph
# @param G graph containing the nodes to be edited
# 
def assign_normal(G):
	# stores the keys of all nodes in a list
	l = list(G.nodes_iter())
	# Loop all nodes in the list to assign the attributes
	for n in l:
		G.node[n]['type'] = 'normal'
		# The initial opinion is given as a random number between 0 and 1
		G.node[n]['opinion']=rd.betavariate(1,1)
	return;