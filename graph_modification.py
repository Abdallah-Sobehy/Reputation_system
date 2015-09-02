## @package graph_modification
# This module contains functions to edit graph contents:
# Adding nodes, edges, attributes...
import networkx as nx
import random as rd
import numpy as np
import operator as op

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


##
# Calculate the maximum absolute change in opinion for all nodes between two conceutive iterations
# @param G_t current updated graph
# @param G_t_1 graph of previous iteration
#
def max_opinion_difference(G_t, G_t_1):
	# store the opinion of nodes in both graphs in two lists
	# store the keys of all nodes in a list
	l_tmp = list(G_t.nodes_iter())
	# use stored keys to access both graphs
	# list of opinions for both graphs initialized to be empty
	l_t = []
	l_t_1 = []
	# for each loop the opinion is added to each of the two lists
	for n in l_tmp:
		l_t += [ G_t.node[n]['opinion'] ]
		l_t_1 += [ G_t_1.node[n]['opinion'] ]
	#subtract opinions and store the differnce in list
	l_diff = list(map(op.sub, l_t, l_t_1))
	# change all values in l_diff list to absolute ones to avoid negative numbers
	i = 0
	for n in l_diff:
		l_diff[i] = abs(n)
		i += 1
	# return the maximum value in l_difference 
	return max(l_diff);

##
# Adding a forceful peer with one of the 4 strategies
# Strategies: Random, Degree, 1/Degree, Degree ^ 2
# @param G graph whch the forceful nodes is to be added to
# @param strategy strategy by which the peer will choose its nodes
# @param budget the number of edges the peer can have
#
def add_forceful(G, strategy, budget):
	n = nx.number_of_nodes(G)
	# Selection of neighbors depeding on chosen strategy
	if strategy == 'random':
		# Create a list of 'budget' random numbers [0, NUM_PEERS]
		f_neighbors = np.random.random_integers(0, n - 1, budget)
		print f_neighbors
	# add the forceful peer to the graph
	G.add_node(n,type = 'f_' + strategy, opinion = 1)
	# iterate the array of neighbors and add an edge
	for i in f_neighbors:
		G.add_edge(n, i)
	return;

##
# colors graph to distinguish between dofferent entities
#
#def color_graph(G):
#	for n in G