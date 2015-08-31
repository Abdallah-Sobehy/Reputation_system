## @package graph_modification
# This module contains functions to edit graph contents:
# Adding nodes, edges, attributes...
import networkx as nx
import random as rd

##
# assign type and opinion attributes to all nodes of the graph as normal peers
# @param G graph containing the nodes to be edited
# 
def assign_normal(G):
	# stores the keys of all nodes in a list
	l = list(G.nodes_iter())
	# Loop all nodes in the list to assign the attributes
	for n in l:
		G.node[n]['type'] = 'normal'
		# The initial opinion is given as a random number between 0 and 1
		G.node[n]['opinion']=rd.betavariate(1,1)#### between -1 and 1, and start in a middle value (0)
	return;

##
# updates local opinion of a node using it's own opinion and neighbor's
# @param G graph of nodes to update its local opinion
# @param alpha weigh given to the opinion of the node itself
#
def local_update(G,alpha):
	# copying an instance of the graph so that the opinion taken into consideration
	# are not the ones updated in the same instance in this function
	G_copy = nx.MultiGraph(G)
	# stores the keys of all nodes in a list
	l = list(G_copy.nodes_iter())
	# Loop all nodes in the list to check for its type
	for n in l:
		if G_copy.node[n]['type'] == 'normal':
			#Iterate and sum all opinions of neighbors
			list_neighbors = list(nx.all_neighbors(G_copy,n))
			# Update opinion only if the node has a neighbor
			if (len(list_neighbors) > 0):
				neighbors_opinion = 0
				for o in list_neighbors:
					neighbors_opinion += G_copy.node[o]['opinion']
				# Local update equation
				G.node[n]['opinion'] = alpha*G_copy.node[n]['opinion'] + ((1-alpha)/G_copy.degree(n))*neighbors_opinion

	return;