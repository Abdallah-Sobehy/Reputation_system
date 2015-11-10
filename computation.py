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
		# Calculate the total weight of all edges connected to i
		edges_weight = 0
		for neighbor in l_neighbors:
			edges_weight += G[i][neighbor]['weight']
		# update A[i,j] if j is a neighbor of i
		for j in range(0,n):
			if j in l_neighbors:
				A[i,j] = (1-alpha)/edges_weight
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
		edges_weight = 0
		for neighbor in G.neighbors(i):
			edges_weight += G[i][neighbor]['weight']
		# fill for the 2 columns (representing connection to forceful peers)
		if n in G.neighbors(i):
			AF[i,0] = ((1-alpha)/edges_weight)*G[i][n]['weight']
		if n+1 in G.neighbors(i):
			AF[i,1] = ((1-alpha)/edges_weight)*G[i][n+1]['weight']
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
	S1_followers_percent = S2_followers_percent = neutral_perc = 0
	for i in range(n):
		if G.node[i]['opinion'] < - neutral_range:
			S2_followers_percent +=1
		elif G.node[i]['opinion'] > neutral_range:
			S1_followers_percent +=1
		elif G.node[i]['opinion'] >= - neutral_range and G.node[i]['opinion'] <= neutral_range:
			neutral_perc +=1
		else:
			try:
				raise ex.UncategorizedNodeError(i)
			except ex.UncategorizedNodeError as un:
					print 'warning a node [',i,'] out of the specifed categories according to opinion'
	S1_followers_percent /= n
	S2_followers_percent /= n
	neutral_perc /= n
	return [S1_followers_percent,S2_followers_percent,neutral_perc]

##
# Updates followers and winning percentages percentages of the two strategies
# @param new_perc Followers for either of the forceful peers in the last match [S1_followers,S2_followers,neutral]
# @param S1_f followers array of the forceful peer with strategy 1 for each match
# @param S2_f followers array of the forceful peer with strategy 2 for each match
# @param neutral array storing percentge of neutral nodes in each match
# @param index array index to be updated in followers' or neutral arrays.
# @param S1_win number of wins of strategy 1 for (index+1) matches 
# @param S1_win number of wins of strategy 2 for (index+1) matches
# @param tie number of tie matches between both for (index+1) matches
# @param index array index to updated for followers and neutral arrays
#
def update_percentages(new_perc,S1_f, S2_f, neutral, index, wins):
	#store each percent in its array
	S1_f[index] = new_perc[0]
	S2_f[index] = new_perc[1]
	neutral[index] = new_perc[2]
	# Update win percentges
	if S1_f[index] > S2_f[index]:
		wins[0] += 1
	elif S2_f[index] > S1_f[index]:
		wins[1] += 1
	else : wins[2] += 1
	return

##
# returns the number of simulations needed for a a given confidence interval (here it is 0.5%)
# Equation used: n = (100*z*s)/r*mean)**2 where z is taken as a constant from gaussian distribution curve 
# for the region (1-alpha/2) where alpha = 0.05, thus, z = 1.96
# s is standard deviation and r is the confidence interval/2 as a percentage of the mean
# @param mean measured mean after simulations
# @param followers_list list containing followers percentage for each simulation for a given strategy
def get_sim_num(mean, followers_list):
	# Compute standard deviation
	s = 0
	for followers in followers_list:
		s += ((followers-mean)**2)
	s *= (1/(len(followers_list)-1))
	s = np.sqrt(s)
	z = 1.96
	# For one percent confidence interval
	r = 0.5
	return ((100*z*s)/(r*mean))**2
##
# returns precision as a percentage of mean given the number of simulations
# Equation used r = (100*z*s)/sqrt(n)*mean) where z is taken as a constant from gaussian distribution curve 
# for the region (1-alpha/2) where alpha = 0.05, thus, z = 1.96
# s is standard deviation and n is the number of simulations done.
# @param mean measured mean after simulations
# @param followers_list list containing followers percentage for each simulation for a given strategy
# @param n is the number of simulations executed.

def get_precision(mean, followers_list, n):
	# Compute standard deviation
	s = 0
	for followers in followers_list:
		s += ((followers-mean)**2)
	s *= (1/(len(followers_list)-1))
	s = np.sqrt(s)
	z = 1.96

	return (100*z*s)/(np.sqrt(n)*mean) 
	

def drange(start, stop, step):
	r = start
	while r < stop:
   		yield r
   		r += step