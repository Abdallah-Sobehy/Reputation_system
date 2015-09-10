## @package computation
# contains functions related to the theoritical proof of convergence equation
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# Also functions relate to calculations for the simulation of different strategies e.g. percentage of positive nodes
from __future__ import division # to allow integer division to produce a floating point
from scipy import linalg
import numpy as np
import networkx as nx

##
# creates the A[normal] matrix that holds the (1-alpha)/deg part of the opinion calculation equation
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# returns a square matrix with zeros in the diagonal and (1-alpha)/deg at indices representing neighbors
# @param G graph from which the A matrix will be extracted
# @param alpha weigh given to self opinion
def mat_A(G, alpha):
	all_peers = nx.number_of_nodes(G)
	# normal peers are all peers except the forceful ones
	n = all_peers - 2
	# initialize array A to zeros
	A = np.zeros(shape=(n,n))
	#iterate all normal nodes in the graph
	for i in range(0,n):
		# store keys of all neighbors in a list
		l_neighbors = G.neighbors(i)
		# store the degree of i
		deg = G.degree(i)
		# update A[i,j] if j is a neighbor of i
		for j in range(0,n):
			if j in l_neighbors:
				A[i,j] = (1-alpha)/deg
	return A;

##
# Calculates A[forceful] matrix which represents the (1-alpha)/deg part where forceful peers are involved
# returns nx2 matrix (where n are normal nodes) 
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# @param G graph under test
# @param alpha wight given to self opinion
#
def mat_AF(G, alpha):
	all_peers = nx.number_of_nodes(G)
	# normal peers are all peers except the forceful ones
	n = all_peers - 2
	# initialize array A to zeros
	AF = np.zeros(shape=(n,2))
	# Iterate for all rows of the matrix
	for i in range(n):
		# fill for the 2 columns (representing connection to forceful peers)
		if n in G.neighbors(i):
			AF[i,0] = ((1-alpha)/G.degree(i))*G.number_of_edges(i,n)
		if n+1 in G.neighbors(i):
			AF[i,1] = ((1-alpha)/G.degree(i))*G.number_of_edges(i,n+1)
	return AF;
##
# creates the h vector that contains the initial opinions of all nodes in the graph multiplied by alpha
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# @param G Graph of nodes to retrieve the opinions from
# @param alpha wwight given to self opinion
#
def vec_h(G, alpha):
	all_peers = nx.number_of_nodes(G)
	# normal peers are all peers except the forceful ones
	n = all_peers - 2
	# initialize vector h to zeros
	h = np.zeros(shape=(n,1))
	#iterate all nodes in the graph
	for i in range(0,n):
		h[i] = G.node[i]['initial_opinion']
	h = h*alpha
	return h;

##
# Calculates R (inf) using the eq R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# @param G graph under test
# @param alpha wight given to self opinion
#
def R_inf(G,alpha):
	all_peers = nx.number_of_nodes(G)
	# normal peers are all peers except the forceful ones
	n = all_peers - 2
	A = mat_A(G, alpha)
	h = vec_h(G,alpha)
	# Identity matrix to be used in the equation
	I = np.identity(n)
	AF = mat_AF(G,alpha)
	# Initial opinion of the forceful peers
	RF = np.array([ [1],[-1] ])

	R = (linalg.inv(I-A)).dot(h+(AF.dot(RF)))
	return R;

##
# Calculates the percentage of normal positive, negative and neutral nodes depending on a given neutral range around 0
# @param G graph to calculate the percentage of different nodes from
# @param neutral_range a number that any node with an opinion between its negative and positive value is considered neutral
# returs a list of three elements storing with the following order:
# [0]positive nodes percentage, [1] negative nodes percentage and [2] neutral nodes percentage 
#
def percentages(G,neutral_range):
	all_peers = nx.number_of_nodes(G)
	# normal peers are all peers except the forceful ones
	n = all_peers - 2
	pos_percent = neg_percent = neutral_perc = 0
	for i in range(n):
		if G.node[i]['opinion'] < - neutral_range:
			neg_percent +=1
		elif G.node[i]['opinion'] > neutral_range:
			pos_percent +=1
		elif G.node[i]['opinion'] >= - neutral_range and G.node[i]['opinion'] <= neutral_range:
			neutral_perc +=1
		else:
			try:
				raise ex.UncategorizedNodeError(i)
			except ex.UncategorizedNodeError as un:
					print 'warning a node [',i,'] out of the specifed categories according to opinion'
	pos_percent /= n
	neg_percent /= n
	neutral_perc /= n
#	print 'Positive nodes: %f\nNegative nodes: %f\nNeutral Nodes: %f' %(pos_percent,neg_percent,neutral_perc)
	return [pos_percent,neg_percent,neutral_perc]