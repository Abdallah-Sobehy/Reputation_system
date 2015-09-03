## @package computation
# contains functions related to the theoritical proof of convergence equation
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
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
			AF[i,0] = (1-alpha)/G.degree(i)
		if n+1 in G.neighbors(i):
			AF[i,1] = (1-alpha)/G.degree(i)
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