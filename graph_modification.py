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
	i = 0
	# Loop all nodes to assign the attributes
	for n in G.nodes_iter():
		G.node[i]['type'] = 'normal'
		# The initial opinion is given as a random number between 0 and 1
		G.node[i]['opinion']=rd.betavariate(1,1)
		i=i+1
	return;