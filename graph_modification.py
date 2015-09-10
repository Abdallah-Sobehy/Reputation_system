## @package graph_modification
# This module contains functions to edit graph contents:
# Adding nodes, edges, attributes...
from __future__ import division # to allow integer division to produce a floating point
import networkx as nx
import random as rd
import numpy as np
import operator as op
import sys
import excp as ex

##
# Create a network graph, of a given type and characteristic
# @param num_peersnumber of noral peers in the graph
# @param proba probability of an edge between any 2 nodes
#
def create_graph(num_peers, proba):
	# Initialize an erdos renyi graph
	initial_graph = nx.erdos_renyi_graph(num_peers,proba)
	# Adding the property of having multiple edges between nodes
	G = nx.MultiGraph(initial_graph)
	# Assign normal peers with type and opinion
	assign_normal(G)
	return G;
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
		# The initial opinion is given as neutral = 0
		G.node[n]['opinion']= 0
		# Storing the value of initial opinion 
		G.node[n]['initial_opinion'] = 0

	return;

##
# Calculates the final opinion vector R_inf by iterations using algorithm 15 in Dr. Amira's thesis
# @param G graph of nodes to update their opinions
# @param ALPHA weight given to self opinion (between 0 and 1)
#
def R_itr(G,ALPHA):
	# The maximum accepted difference of opinions between two iterations.iterations terminated when reached
	THRESHOLD = 0.00001
	# maximum difference variable to indicate the change in opinion after local update
	max_diff = 1
	# Loop to call Local update function until max difference is less than the threshold
	# @var num_loops nuber of loops needed until conversion
	num_loops = 0
	while (max_diff > THRESHOLD):
		# copying an instance of the graph
		G_copy = nx.MultiGraph(G)
		local_update(G,ALPHA)
		max_diff = max_opinion_difference(G, G_copy)
		num_loops += 1
#	print 'The maximum difference = ', max_diff
#	print 'number of loops until conversion = ', num_loops
	# R_itr contains opinion of nodes due to iterations
	R_itr = []
	for n in range(G.number_of_nodes()-2):
		R_itr += [[ G.node[n]['opinion']] ]
	return R_itr;



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
		# Update is only done to normal peers.
		if G_copy.node[n]['type'] == 'normal':
			#Iterate and sum all opinions of neighbors
			list_neighbors = list(nx.all_neighbors(G_copy,n))
			# Update opinion only if the node has a neighbor
			if (len(list_neighbors) > 0):
				neighbors_opinion = 0
				for o in list_neighbors:
					#num_edges = 1
					num_edges = G.number_of_edges(n,o)
					neighbors_opinion += num_edges*G_copy.node[o]['opinion']
				# Local update equation
				G.node[n]['opinion'] = alpha*G.node[n]['initial_opinion'] + ((1-alpha)/G_copy.degree(n))*neighbors_opinion

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
# Adding 2 forceful peers with one of the 4 strategies each
# Strategies: Random, Degree, 1/Degree, Degree ^ 2
# @param G graph whch the forceful nodes is to be added to
# @param strategy1 strategy by first forceful peer by which it will choose its nodes
# @param budget1 the number of edges the first forceful peer can have
# @param strategy2 strategy by second forceful peer by which it will choose its nodes
# @param budget2 the number of edges the second forceful peer can have
#
def add_forceful(G, strategy1, budget1, strategy2, budget2):
	n = nx.number_of_nodes(G)
	# Selection of neighbors depending on chosen strategy for forceful peer 1
	if strategy1 == 'random':
		# Create a list of 'budget' random numbers [0, NUM_PEERS]
		f1_neighbors = np.random.random_integers(0, n - 1, budget1)
	elif strategy1 == 'D':
		# call strategy_D function to calculate neighbors of forceful peer 1
		f1_neighbors = strategy_D(G,budget1)
	elif strategy1 == 'D^2':
		# call strategy_D2 function to calculate neighbors for forceful peer 1
		f1_neighbors = strategy_D2(G, budget1)
	elif strategy1 == '1/D':
		# call strategy_1_D function to calculate neighbors for forceful peer 1
		f1_neighbors = strategy_1_D(G, budget1)
	else:
		raise SystemExit('Chosen strategy for first forceful peer [[' + strategy1+ ']] is not applicable\nprogram will exit');

	# Selection of the neighbors depending on the strategy for peer 2
	if strategy2 == 'random':
		# Create a list of 'budget1' random numbers [0, NUM_PEERS]
		f2_neighbors = np.random.random_integers(0, n - 1, budget2)	
	elif strategy2 == 'D':
		# call strategy_D function to calculate neighbors of forceful 2
		f2_neighbors = strategy_D(G,budget2)
	elif strategy2 == 'D^2':
		# call strategy_D2 function to calculate neighbors of forceful 2
		f2_neighbors = strategy_D2(G,budget2)
	elif strategy2 == '1/D':
		# call strategy_1_D function to calculate neighbors of forceful 2
		f2_neighbors = strategy_1_D(G,budget2)
	# an Error statement if the chosen strategy is not applicable
	else:
		raise SystemExit('Chosen strategy for second forceful peer [[' + strategy2+ ']] is not applicable\nprogram will exit');

	# add the forceful peers to the graph, the first is with opinion 1 
	# The second is with opinion -1
	G.add_node(n,type = 'f_' + strategy1, opinion = 1)
	G.add_node(n+1,type = 'f_' + strategy2, opinion = -1)
	# iterate the array of neighbors and add an edge
	for i in f1_neighbors:
		G.add_edge(n, i)
	for i in f2_neighbors:
		G.add_edge(n+1,i)
	return;

##
# returns a list of neighbors for a forceful peer with D strategy
# @param G graph with nodes from which the forceful peer will choose
# @param budget number of neighbors the forceful peer will choose
#
def strategy_D(G, budget):
	# limits is a list that stores floats between 0 and one which defines
	# the probabaility of choosing a certain node depending on its degree
	limits = [0.0]
	num_edges = G.number_of_edges()
	# iterate nodes to calculate limits depending on degree
	for i in G:
		limits += [G.degree(i)/(2*num_edges) + limits[i]]
	return select_neighbors(limits, budget)

##
# returns a list of neighbors for a forceful peer with D^2 strategy
# @param G graph with nodes from which the forceful peer will choose
# @param budget number of neighbors the forceful peer will choose
#
def strategy_D2(G, budget):
	# limits is a list that stores floats between 0 and one which defines
	# the probabaility of choosing a certain node depending on its degree
	limits = [0.0]
	# store the degree of all nodes in a list
	degrees = G.degree()
	tmp = []
	for i in range(len(degrees)):
		tmp += [degrees[i]]
	# squaring all degrees in the list
	degrees2 = [x**2 for x in tmp]	
	# summation of (degrees^2) for all nodes
	sum_degs2 = sum(degrees2)
	# iterate nodes to calculate limits depending on degree
	for i in G:
		limits += [(G.degree(i)** 2)/sum_degs2 + limits[i]]
	return select_neighbors(limits, budget)

##
# returns a list of neighbors for a forceful peer with 1/D strategy
# @param G graph with nodes from which the forceful peer will choose
# @param budget number of neighbors the forceful peer will choose
#
def strategy_1_D(G, budget):
	# limits is a list that stores floats between 0 and one which defines
	# the probabaility of choosing a certain node depending on its degree
	limits = [0.0]
	# store the degree of all nodes in a list
	degrees = G.degree()
	tmp = []
	for i in range(len(degrees)):
		tmp += [degrees[i]] 
	# computes the reciprocal of all degrees
	degrees_recp = []

	for i in range(len(tmp)):
		degrees_recp += [1/tmp[i]]

	# summation of all reciprocals
	sum_degs_recp = sum(degrees_recp)
	for i in G:
		try:
			limits += [((1/G.degree(i))/sum_degs_recp) + limits[i]]
		except ZeroDivisionError:
			sys.exit('Division by zero when calculating neighbors for 1/D strategy\ndue to the presence of a node with zero degree')
	return select_neighbors(limits, budget)

##
# returns of selected nodes to be neighbors of a forceful peer
# depending on the given limits list
#
def select_neighbors(limits, budget):
	# list to contain keys of neighbors t be attached to the forceful peer
	f_neighbors = []
	# iterate budget times to add neighbors to the list
	for i in range(budget):
		rnd = np.random.random()
		# compare the random number to the limits and add node accordingly
		for j in range(len(limits) - 1):
			if rnd >= limits[j] and rnd < limits[j+1]:
				f_neighbors += [j]
	return f_neighbors;