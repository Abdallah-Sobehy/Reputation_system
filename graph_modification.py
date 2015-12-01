## @package graph_modification
# This module contains functions to edit graph contents:
# Adding nodes, edges, attributes...
from __future__ import division # to allow integer division to produce a floating point
import networkx as nx
import random as rd
import numpy as np
import operator as op
import sys
import pulp
import excp as ex
import math as m

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
		G = nx.erdos_renyi_graph(num_peers,g_char)
	elif g_type == 'geometric':
		# Initialize a random geometric graph with radius g_char
		G = nx.random_geometric_graph(num_peers,g_char)
	elif g_type == 'barabasi_albert':
		# Initialize a barbasi albert graph with g_char starting nodes
		G = nx.barabasi_albert_graph(num_peers,g_char)
	else : raise SystemExit('Chosen graph type ['+str(g_type)+'] is not applicable.\nProgram will terminate')
	# Adding the property of having multiple edges between nodes
	#G = nx.MultiGraph(G)
	for e in G.edges_iter():
		G[e[0]][e[1]]['weight'] = 1
	G.graph['type']= g_type
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
	#print 'The maximum difference = ', max_diff
	#print 'number of loops until conversion = ', num_loops
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
				# the total weight of all edges connected to node n
				edges_weight = 0
				for o in list_neighbors:
					neighbors_opinion += G[n][o]['weight']*op_list[o]
					edges_weight += G[n][o]['weight']
				# Local update equation
				G.node[n]['opinion'] = alpha*G.node[n]['initial_opinion'] + ((1-alpha)/edges_weight)*neighbors_opinion
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
# @param G graph which the forceful peer is to be added to
# @param strategy1 strategy by first forceful peer by which it will choose its neighbors
# @param budget1 the total edge weights the first forceful peer can have
# @param strategy2 strategy by second forceful peer by which it will choose its neighbors
# @param budget2 the total edge weights the second forceful peer can have
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
	G.add_node(n,type = strategy1, opinion = 1)
	G.add_node(n+1,type = strategy2, opinion = -1)
	# iterate the array of neighbors and add an edge
	for i in f1_neighbors:
		# If an edge already exists between the 2 nodes increase the weight.
		if G.number_of_edges(n,i) > 0: 
			G[n][i]['weight'] +=1
		else:G.add_edge(n, i, weight = 1)
	for i in f2_neighbors:
		# If an edge already exists between the 2 nodes increase the weight.
		if G.number_of_edges(n+1,i) > 0:
			G[n+1][i]['weight'] +=1
		else: G.add_edge(n+1,i, weight = 1)
	return;

##
# Adding one forceful peers with one of the 4 strategies each
# Strategies: Random, Degree, 1/Degree, Degree ^ 2
# This function assumes no forceful peer has already been added to the graph
# @param G graph which the forceful peer is to be added to
# @param strategy strategy of the forceful peer by which it will choose its neigbors
# @param budget the total edge weights the forceful peer can have
#
def add_one_forceful(G, strategy, budget):
	n = nx.number_of_nodes(G)
	# Selection of neighbors depending on chosen strategy for forceful peer
	if strategy == 'random':
		# Create a list of 'budget' random numbers [0, NUM_PEERS]
		f_neighbors = np.random.random_integers(0, n - 1, budget)
	elif strategy == 'D':
		# call strategy_D function to calculate neighbors of forceful peer
		f_neighbors = strategy_D(G,budget)
	elif strategy == 'D^2':
		# call strategy_D2 function to calculate neighbors for forceful peer
		f_neighbors = strategy_D2(G, budget)
	elif strategy == '1/D':
		# call strategy_1_D function to calculate neighbors for forceful peer
		f_neighbors = strategy_1_D(G, budget)
	else:
		raise SystemExit('Chosen strategy for forceful peer [[' + strategy1+ ']] is not applicable\nprogram will exit');

	# add the forceful peers to the graph, with opinion 1 
	G.add_node(n,type = strategy, opinion = -1)
	# iterate the array of neighbors and add an edge
	for i in f_neighbors:
		# If an edge already exists between the 2 nodes increase the weight.
		if G.number_of_edges(n,i) > 0: 
			G[n][i]['weight'] +=1
		else:G.add_edge(n, i, weight = 1)
	return;
##
# Adds a smart peer to the graph with minmum possible connections to beat the alread existing peer
# Linear programming is used.
# @param G graph with normal peer and one frceful peer that is already connected
def add_smart(G,alpha, budget, neutral_range):
	normal = G.number_of_nodes() - 1
	# Compute the number of binary bits needed to store the largest possible weight which depends on the budget
	num_bits = len("{0:b}".format(budget))
	#initialise the model
	win_with_min = pulp.LpProblem('Beat existing peer with min budget',pulp.LpMinimize)
	# Parameters 
	# edge weight between normal nodes and existing forceful
	weight_existing = []
	for i in xrange(normal):
		if (G.has_edge(normal,i)):
			weight_existing.append(G[normal][i]['weight'])
		else: weight_existing.append(0)
	#print weight_existing
	# normal neighbors to each node
	sub_g = G.subgraph(xrange(normal))
	neighbors = []
	for i in xrange(normal):
		neighbors.append(sub_g.neighbors(i))
	#print neighbors
	# Define the variables for the LP, the weight from the smart peer to all normal nodes
	x = pulp.LpVariable.dict('weight to %d', xrange(normal), lowBound = 0,cat = pulp.LpInteger)
	# Binary representation of edge weights, used to linearize equations
	z0 = pulp.LpVariable.dict('z0 bin weight to 0',xrange(num_bits), lowBound = 0, upBound=1,  cat= pulp.LpBinary)
	z1 = pulp.LpVariable.dict('z1 bin_weight to 1',xrange(num_bits), lowBound = 0, upBound=1, cat= pulp.LpBinary)
	z2 = pulp.LpVariable.dict('z2 bin_weight to 2',xrange(num_bits), lowBound = 0, upBound=1, cat= pulp.LpBinary)
	z3 = pulp.LpVariable.dict('z3 bin_weight to 3',xrange(num_bits), lowBound = 0, upBound=1, cat= pulp.LpBinary)
	z4 = pulp.LpVariable.dict('z4 bin_weight to 4',xrange(num_bits), lowBound = 0, upBound=1, cat= pulp.LpBinary)
	# Opinion 
	variableNames = ['y0','y1','y2','y3','y4']
	yvars = [pulp.LpVariable(name,-1,1,cat = 'Continous') for name in variableNames]
	# y0 = pulp.LpVariable('opinion of 0',-1,1) 
	# y1 = pulp.LpVariable('opinion of 1',-1,1) 
	# y2 = pulp.LpVariable('opinion of 2',-1,1) 
	# y3 = pulp.LpVariable('opinion of 3',-1,1) 
	# y4 = pulp.LpVariable('opinion of 4',-1,1) 
	# Intermediate variable for linearity reasons (to escape y*x)
	t0 = pulp.LpVariable.dict('Intermediate 0',xrange(num_bits),lowBound = 0, cat = 'Continous')
	t1 = pulp.LpVariable.dict('Intermediate 1',xrange(num_bits),lowBound = 0, cat = 'Continous')
	t2 = pulp.LpVariable.dict('Intermediate 2',xrange(num_bits),lowBound = 0, cat = 'Continous')
	t3 = pulp.LpVariable.dict('Intermediate 3',xrange(num_bits),lowBound = 0, cat = 'Continous')
	t4 = pulp.LpVariable.dict('Intermediate 4',xrange(num_bits),lowBound = 0, cat = 'Continous')

	# Intermediate variable = 1 if following smart, 0 if neutral or following existing forceful
	variableNames = ['p0','p1','p2','p3','p4']
	pvars = [pulp.LpVariable(name,0,1, cat = 'Integer') for name in variableNames]
	# Objective function
	win_with_min += sum ([x[i] for i in xrange(normal)])

	# constraints
	# To win with at least an equal budge to the opponent
	#win_with_min += sum ([x[i] for i in xrange(normal)]) <= budget
	# binary representation of edges
	win_with_min += sum ([z0[i]*m.pow(2,i) for i in xrange(num_bits)]) == x[0]
	win_with_min += sum ([z1[i]*m.pow(2,i) for i in xrange(num_bits)]) == x[1]
	win_with_min += sum ([z2[i]*m.pow(2,i) for i in xrange(num_bits)]) == x[2]
	win_with_min += sum ([z3[i]*m.pow(2,i) for i in xrange(num_bits)]) == x[3]
	win_with_min += sum ([z4[i]*m.pow(2,i) for i in xrange(num_bits)]) == x[4]
	# Opinion and intermediate constraints
	win_with_min += sum ([t0[i]*m.pow(2,i) for i in xrange(num_bits)]) + yvars[0]*(weight_existing[0]+ len(neighbors[0])) == (1-alpha)*(sum([ yvars[i] for i in neighbors[0]]) - weight_existing[0] + x[0])
	win_with_min += sum ([t1[i]*m.pow(2,i) for i in xrange(num_bits)]) + yvars[1]*(weight_existing[1]+ len(neighbors[1])) == (1-alpha)*(sum([ yvars[i] for i in neighbors[1]]) - weight_existing[1] + x[1])
	win_with_min += sum ([t2[i]*m.pow(2,i) for i in xrange(num_bits)]) + yvars[2]*(weight_existing[2]+ len(neighbors[2])) == (1-alpha)*(sum([ yvars[i] for i in neighbors[2]]) - weight_existing[2] + x[2])
	win_with_min += sum ([t3[i]*m.pow(2,i) for i in xrange(num_bits)]) + yvars[3]*(weight_existing[3]+ len(neighbors[3])) == (1-alpha)*(sum([ yvars[i] for i in neighbors[3]]) - weight_existing[3] + x[3])
	win_with_min += sum ([t4[i]*m.pow(2,i) for i in xrange(num_bits)]) + yvars[4]*(weight_existing[4]+ len(neighbors[4])) == (1-alpha)*(sum([ yvars[i] for i in neighbors[4]]) - weight_existing[4] + x[4])

	for j in xrange(num_bits):
		win_with_min += t0[j] >= -z0[j]
		win_with_min += t0[j] <= z0[j]
		win_with_min += t0[j] >= yvars[0] - 1 +z0[j]
		win_with_min += t0[j] <= yvars[0] + 1 -z0[j]


	for j in xrange(num_bits):
		win_with_min += t1[j] >= -z1[j]
		win_with_min += t1[j] <= z1[j]
		win_with_min += t1[j] >= yvars[1] - 1 +z1[j]
		win_with_min += t1[j] <= yvars[1] + 1 -z1[j]

	for j in xrange(num_bits):
		win_with_min += t2[j] >= -z2[j]
		win_with_min += t2[j] <= z2[j]
		win_with_min += t2[j] >= yvars[2] - 1 +z2[j]
		win_with_min += t2[j] <= yvars[2] + 1 -z2[j]

	for j in xrange(num_bits):
		win_with_min += t3[j] >= -z3[j]
		win_with_min += t3[j] <= z3[j]
		win_with_min += t3[j] >= yvars[3] - 1 +z3[j]
		win_with_min += t3[j] <= yvars[3] + 1 -z3[j]

	for j in xrange(num_bits):
		win_with_min += t4[j] >= -z4[j]
		win_with_min += t4[j] <= z4[j]
		win_with_min += t4[j] >= yvars[4] - 1 +z4[j]
		win_with_min += t4[j] <= yvars[4] + 1 -z4[j]

	for i in xrange(normal):
		win_with_min += yvars[i] >= -1 + pvars[i]*(1+neutral_range)

	win_with_min += sum ([pvars[i] for i in xrange(normal)]) >= m.ceil(normal/2)
	#win_with_min += x[0] ==3 
	win_with_min.solve()
	for node in xrange(normal):
		print 'weight to %d is %d' %(node,x[node].value())
	for i in z0:
		print z0[i].value()
	# for i in z1:
	# 	print z1[i].value()
	# for i in z2:
	# 	print z2[i].value()
	# for i in z3:
	# 	print z3[i].value()

	# for i in z4:
	# 	print z4[i].value()
	print 'tij: '
	for i in t0:
		print t0[i].value()
	print '--------'
	for i in t1:
		print t1[i].value()
	print '--------'
	for i in t2:
		print t2[i].value()
	print '--------'
	for i in t3:
		print t3[i].value()
	print '--------'
	for i in t4:
		print t4[i].value()
	print '--------'

	print 'yvars'
	for i in xrange(len(yvars)):
		print 'y' + str(i) + ':' + str(yvars[i].value())
		print '--------'
	G.add_node(6,type = 'smart', opinion = 1)
	# iterate the array of neighbors and add an edge
	f_neighbors = [0,1]
	for i in f_neighbors:
		G.add_edge(6, i, weight = 1)
	
##
# Adds a forceful peer that is connected to all normal peers with a given weight
# @param G input graph
# @param lamda the weight of each edge from the forceful peer
#
def connect_to_all(G,lamda):
	forceful_key = G.number_of_nodes()
	G.add_node(forceful_key, type = 'smart', opinion = -1)
	for n in G.nodes_iter():
		# Connect an edge only with a normal node
		if G.node[n]['type'] == 'normal':
			G.add_edge(forceful_key,n, weight = lamda)


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
	# limits is a list that stores floats between 0 and 1	 which defines
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
