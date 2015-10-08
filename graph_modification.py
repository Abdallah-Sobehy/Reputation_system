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
# @param g_char graph charateristic that depends on the graph type
# For a random graph: probability of an edge between any 2 nodes
# For a geometric graph maximum euclidean distance for a edge to exist between 2 nodes
#
def create_graph(g_type,num_peers, g_char):
	if g_type == 'random':
		# Initialize an erdos renyi graph with probability g_char
		initial_graph = nx.erdos_renyi_graph(num_peers,g_char)
	elif g_type == 'geometric':
		# Initialize a random geometric graph with radius g_char
		initial_graph = nx.random_geometric_graph(num_peers,g_char)
	elif g_type == 'barabasi_albert':
		# Initialize a barbasi albert graph with g_char starting nodes
		initial_graph = nx.barabasi_albert_graph(num_peers,g_char)
	else : raise SystemExit('Chosen graph type ['+str(g_type)+'] is not applicable.\nProgram will terminate')
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
		# storing opinion values in a list before update at (t-1)
		op_list_t_1 = get_opinion(G)
		local_update(G,ALPHA)
		# storing opinions after update at time t
		op_list_t = get_opinion(G)
		max_diff = max_opinion_difference(op_list_t, op_list_t_1)
		num_loops += 1
#	print 'The maximum difference = ', max_diff
#	print 'number of loops until conversion = ', num_loops
	# R_itr contains opinion of nodes due to iterations
	R_itr = []
	for n in range(G.number_of_nodes()-2):
		R_itr.append([G.node[n]['opinion']])
	return R_itr;

##
# updates local opinion of a node using it's own opinion and neighbor's
# @param G graph of nodes to update its local opinion
# @param alpha weigh given to the opinion of the node itself
#
def local_update(G,alpha):
	# storing opinions of all nodes in a list to avoid using updated opinions of neighbors in the process
	op_list = get_opinion(G)
	# Loop all nodes in the graph
	for n in G:
		# Update is only done to normal peers.
		if G.node[n]['type'] == 'normal':
			#Iterate and sum all opinions of neighbors
			list_neighbors = list(nx.all_neighbors(G,n))
			# Update opinion only if the node has at least one neighbor
			if (len(list_neighbors) > 0):
				neighbors_opinion = 0
				for o in list_neighbors:
					num_edges = G.number_of_edges(n,o)
					neighbors_opinion += num_edges*op_list[o]
				# Local update equation
				G.node[n]['opinion'] = alpha*G.node[n]['initial_opinion'] + ((1-alpha)/G.degree(n))*neighbors_opinion

	return;


##
# Calculate the maximum absolute change in opinion for all nodes between two conceutive iterations
# @param l_t opinion list of current updated graph
# @param G_t_1 opinion +=list of previous iteration
#
def max_opinion_difference(l_t, l_t_1):
	#subtract opinions and store the absolute difference in list
	l_diff = []
	for i in range(len(l_t)):
		l_diff.append(abs(l_t[i] - l_t_1[i]))
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
		limits.append(G.degree(i)/(2*num_edges) + limits[i])
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
		tmp.append(degrees[i])
	# squaring all degrees in the list
	degrees2 = [x**2 for x in tmp]	
	# summation of (degrees^2) for all nodes
	sum_degs2 = sum(degrees2)
	# iterate nodes to calculate limits depending on degree
	for i in G:
		limits.append((G.degree(i)** 2)/sum_degs2 + limits[i])
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
		tmp.append(degrees[i]) 
	# computes the reciprocal of all degrees
	degrees_recp = []

	for i in range(len(tmp)):
		degrees_recp.append(1/tmp[i])

	# summation of all reciprocals
	sum_degs_recp = sum(degrees_recp)
	for i in G:
		try:
			limits.append( ((1/G.degree(i))/sum_degs_recp) + limits[i] )
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
				f_neighbors.append(j)
	return f_neighbors;

##
# Helping function to get the opinions of nodes in a graph
# @param G graph to extract the opinion of its nodes
# returns list of opinions
#
def get_opinion(G):
	op_list = []
	for i in G:
		op_list.append(G.node[i]['opinion'])
	return op_list;
